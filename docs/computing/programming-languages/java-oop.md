# Java OOP

Object-oriented programming in Java is easiest to learn if you do not start from abstract buzzwords. Start with one practical question instead:

How do we model a thing with data and behavior so that the code stays organized as the program grows?

That question leads naturally to classes, objects, encapsulation, inheritance, interfaces, and polymorphism.

## Class vs Object

A `class` is the blueprint. An `object` is a concrete instance created from that blueprint.

```java
class Cookie {
    String flavor;
}

Cookie chocolate = new Cookie();
```

Useful beginner analogy:

- class = cookie cutter
- object = actual cookie produced from it

## Properties and Methods

Classes usually contain:

- properties / fields for data
- methods for behavior

```java
class Car {
    String color;

    void drive() {
        System.out.println("Driving");
    }
}
```

This is the first practical OOP move: keep related data and actions together.

## Constructors

A constructor runs when an object is created. It has the same name as the class and no return type.

```java
class Passport {
    String firstName;
    String lastName;

    Passport(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
}
```

Why constructors matter:

- they establish valid initial state
- they reduce half-initialized objects
- they make object creation more explicit

## `this`

`this` refers to the current object instance.

It is especially common in constructors and setters when parameter names match field names.

```java
class Car {
    String model;

    Car(String model) {
        this.model = model;
    }
}
```

Key point: `this.model` means "the field on this object", while plain `model` can refer to the method parameter.

## Void vs Non-Void Methods

Methods either return data or they do not.

```java
class Car {
    void start() {
        System.out.println("Started");
    }

    String getStatus() {
        return "running";
    }
}
```

- `void` methods perform an action
- non-`void` methods return a value

## Encapsulation

Encapsulation means hiding internal details behind a controlled public surface.

Practical intuition:

- outside code should use exposed operations
- internal representation should stay protected

```java
class Car {
    private String model;

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }
}
```

This is why `private` fields plus public getters/setters appear so often in Java code.

## Access Modifiers

At this level, the most important modifiers are:

| Modifier | Meaning |
| -------- | ------- |
| `public` | accessible broadly |
| `private` | accessible only inside the class |
| `static` | belongs to the class rather than an instance |

Example:

```java
class Car {
    public static int wheels = 4;
    private String model;
}
```

Key point: `static` is not really an access modifier in the same sense as `public` and `private`, but beginners often first encounter it alongside them because it changes how a member is used.

## Inheritance

Inheritance is for sharing common structure and behavior across related classes.

```java
class Car {
    String model;

    void drive() {
        System.out.println("Driving");
    }
}

class Toyota extends Car {
}
```

This lets `Toyota` reuse what already exists in `Car`.

Good use of inheritance usually means:

- there is a real shared concept
- the subclass is genuinely a specialized form of the base class

## Base Class and Subclass

Common vocabulary:

- base class / superclass: the class being extended
- subclass: the class that inherits from it

Inheritance helps centralize duplicated code, but it can also create awkward models if the parent class is too broad or badly designed.

## Abstract Classes

An abstract class exists to define common structure without allowing direct instantiation.

```java
abstract class Car {
    abstract void drive();

    void honk() {
        System.out.println("Beep");
    }
}
```

Important rules:

- abstract classes cannot be instantiated directly
- abstract methods have no implementation in that class
- concrete subclasses must implement inherited abstract methods

This is useful when the parent concept is real in design, but incomplete on its own.

## Interfaces

Interfaces are for capabilities or contracts.

```java
interface ElectricCar {
    void charge();
}
```

A class uses an interface with `implements`.

```java
class Tesla extends Car implements ElectricCar {
    @Override
    void drive() {
        System.out.println("Driving electric car");
    }

    @Override
    public void charge() {
        System.out.println("Charging");
    }
}
```

Why interfaces matter:

- they let classes promise behavior
- they reduce the need to inherit unrelated fields or implementation
- they support more flexible design than forcing everything through one inheritance tree

## Why Interfaces Help Where Inheritance Can Fail

Inheritance gives you all inherited members, whether they all fit or not.

Interfaces let you model selective capabilities instead.

This is the key design intuition:

- inheritance answers "is-a"
- interfaces often answer "can-do"

## Polymorphism

Polymorphism means one general type can refer to different concrete forms.

```java
Car myCar = new Tesla();
myCar.drive();
```

Even though the variable is typed as `Car`, the actual method implementation used at runtime can come from `Tesla`.

This is one of the biggest reasons OOP can reduce conditional complexity.

## Overriding

Overriding means a subclass provides its own implementation of an inherited method.

```java
class Toyota extends Car {
    @Override
    void drive() {
        System.out.println("Toyota driving");
    }
}
```

`@Override` is helpful because it makes intent explicit and lets the compiler catch certain mistakes.

## Overloading

Overloading means reusing the same method name with different parameter lists.

```java
class Toyota {
    void drive() {
        System.out.println("Drive normally");
    }

    void drive(int speed) {
        System.out.println("Drive at " + speed);
    }
}
```

Constructors can also be overloaded.

```java
class Honda {
    Honda() {
    }

    Honda(String model) {
    }
}
```

Key point: overriding changes behavior across inheritance; overloading changes which signature is selected.

## Interview Fast Answer

If someone asks for the practical meaning of OOP in Java, a good short answer is:

- classes model entities
- objects are instances with state
- methods define behavior
- encapsulation hides internals
- inheritance and interfaces support reuse and abstraction
- polymorphism lets one general type work with many concrete implementations

If the follow-up asks for the most commonly confused pairs, the highest-signal ones are:

- class vs object
- overriding vs overloading
- abstract class vs interface
- `public` vs `private`
- instance member vs `static` member

## Common Traps

- treating inheritance as the default reuse mechanism for everything
- exposing fields as `public` too early
- mixing up overriding and overloading
- forgetting that constructors do not have return types
- using abstract classes when the real need is just a capability contract
- assuming `static` members belong to each object instance

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Objects and Packages](java-objects-and-packages.md)
- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
