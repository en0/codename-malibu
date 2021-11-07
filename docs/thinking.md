# Game Object

## Component Update Method

3 primary update methods
- PreUpdate
- Update
- PostUpdate
- Triggers 

Each update function will receive the world as an argument
except triggers which only receive the argument details.

A component should register 0 or more update methods when set_parent is called.

## Component Registration

The Container object will offer a registration
method that accepts a registration enumeration.

### RegisterEnum

- BEFORE_UPDATE
- ON_UPDATE
- AFTER_UPDATE

The Container object will offer a Subscribe 
method that accepts a list of triggers that
the component wishes to be notified about.

