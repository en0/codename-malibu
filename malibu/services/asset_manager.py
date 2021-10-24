import pkg_resources
from yaml import safe_load
from typing import Generator, Dict, Union, List

from ..typing import IAssetService
from ..models import AudioSpec, MapSpec, ObjectSpec, ObjectData
from ..mixins import LoggerMixin


class AssetManager(LoggerMixin, IAssetService):

    _pkgname = "malibu"
    _index_file = "assets/index.yaml"
    _audio_specs: Dict[str, AudioSpec]
    _map_specs: Dict[str, MapSpec]
    _object_specs: Dict[str, ObjectSpec]

    def get_map_spec(self, name: str) -> MapSpec:
        return self._map_specs[name]

    def get_audio_spec(self, name: str) -> AudioSpec:
        return self._audio_specs.get(name)

    def iter_audio_specs(self) -> Generator[AudioSpec, None, None]:
        for value in self._audio_specs.values():
            yield value

    def get_object_spec(self, name: str) -> ObjectSpec:
        return self._object_specs.get(name)

    def get_object_data(self, spec: Union[str, ObjectSpec]) -> ObjectData:
        if not isinstance(spec, ObjectSpec):
            spec = self.get_object_spec(spec)
        self.log.info("Loading Object Data: %s", spec.path)
        with pkg_resources.resource_stream(self._pkgname, spec.path) as fd:
            return ObjectData.parse(safe_load(fd))

    def initialize(self):
        self.log.info("Loading Index: %s:%s", self._pkgname, self._index_file)
        with pkg_resources.resource_stream(self._pkgname, self._index_file) as fd:
            dat = safe_load(fd)

        self._initialize_audio_spec(dat)
        self._initialize_map_spec(dat)
        self._initialize_object_spec(dat)

    def _initialize_audio_spec(self, dat: dict):
        self._audio_specs = {}
        for audio_spec in [AudioSpec.parse(raw) for raw in dat["audio"]]:
            audio_spec.path = pkg_resources.resource_filename(self._pkgname, audio_spec.path)
            self.log.debug("Parsing Audio Spec: %s", audio_spec)
            self._audio_specs[audio_spec.name] = audio_spec

    def _initialize_map_spec(self, dat: dict):
        self._map_specs = {}
        for map_spec in [MapSpec.parse(raw) for raw in dat["world-map"]]:
            map_spec.path = pkg_resources.resource_filename(self._pkgname, map_spec.path)
            self.log.debug("Parsing WorldMap Spec: %s", map_spec)
            self._map_specs[map_spec.name] = map_spec

    def _initialize_object_spec(self, dat: dict):
        self._object_specs = {}
        for object_spec in [ObjectSpec.parse(raw) for raw in dat["objects"]]:
            object_spec.parse = pkg_resources.resource_filename(self._pkgname, object_spec.path)
            self.log.debug("Parsing Object Spec: %s", object_spec)
            self._object_specs[object_spec.name] = object_spec

