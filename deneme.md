# MESOP Overview

## Features

- Can be deployed to containers as standalone server
- Provides a fast build-edit-refresh loop through hot reload
- Enables developers to benefit from the mature Angular web framework and Angular Material components
- Provides a flexible and composable components API that's idiomatic to Python
- Easy to deploy by using standard HTTP technologies like Server-Sent Events
- Right now, only Box and Text are thin wrappers around native HTML elements

## Initial Page Load

When a user visits a Mesop application, the following happens:

1. The user visits a path on the Mesop application, e.g., "/" (root path), in their browser.
2. The Mesop client-side web application (Angular) is bootstrapped and sends an InitRequest to the server.
3. The Mesop server responds with a RenderEvent which contains a fully instantiated component tree.
4. The Mesop client renders the component tree. Every Mesop component instance corresponds to 1 or more Angular component instance.

## User Interactions

If the user interacts with the Mesop application (e.g., click a button), the following happens:

1. The user triggers a UserEvent which is sent to the server. The UserEvent includes:
   - The application state (represented by the States proto)
   - The event handler id to trigger
   - The key of the component interacted with (if any)
   - The payload value (e.g., for checkbox, it's a bool value which represents the checked state of the checkbox)
2. The server does the following:
   - Runs a first render loop in tracing mode (i.e., instantiate the component tree from the root component of the requested path). This discovers any event handler functions. In the future, this trace can also be used to calculate the before component tree so we can calculate the diff of the component tree to minimize the network payload.
   - Updates the state by feeding the user event to the event handler function discovered in the previous step.
   - Note: there's a mapping layer between the UserEvent proto and the granular Python event type. This provides a nicer API for Mesop developers then the internal proto representation.
   - Runs a second render loop to generate the new component tree given the new state. After the first render loop, each render loop results in a RenderEvent sent to the client.
   - In the streaming case, we may run the render loop and flush it down via Server-Sent Events many times.
   - The client re-renders the Angular application after receiving each RenderEvent.

## Web Client

Mesop's Web client consists of three main parts:

- **Core**: Includes the root Angular component and singleton services like Channel. This part is fairly small and is the critical glue between the rest of the client layer and the server.
- **Mesop Components**: Every Mesop component has its own directory under `/components`.
  - Note: this includes both the Python API and the Angular implementation for developer convenience.
- **Dev Tools**: Mesop also comes with a basic set of developer tools, namely the components and log panels.
  - The components panel allows Mesop developers to visualize the component tree.
  - The log panel allows Mesop developers to inspect the application state and component tree values.

## Nested State

Example of nested state usage:

```python
class NestedState:
    val: str
    num: int

@me.stateclass
class State:
    nested: NestedState
    text: str
    
No need to re-run the code after saving it.

**Important:** MUST USE UNMUTABLE values in stateclass. If you're using mutable, you must not use default values.

The following will raise an exception because dataclasses prevent you from using mutable collection types like list as the default value because this is a common footgun:

```python
@me.stateclass
class State:
    a: list[str] = ["abc"]

If you want a default of an empty list, you can just not define a default value and Mesop will automatically define an empty list default value. For example:

@me.stateclass
class State:
    a: list[str]

Its the equivalent of:

@me.stateclass
class State:
    a: list[str] = field(default_factory=list)

Tip: You must have a yield statement as the last line of a generator event handler function. Otherwise, any code after the final yield will not be executed.

Alternative Tools
Streamlit: If you need to quickly build a data-driven application or dashboard.
Shiny: For interactive data visualization similar to R's Shiny.
PyWebIO Overview
PyWebIO is a Python framework for building web applications without requiring frontend code. It allows developers to focus on backend logic while providing pre-built widgets for the UI.

Key Features
Low Code: Simplifies the development process with minimal code.
Pre-built Widgets: Includes a variety of widgets for creating interactive UIs.
Fast Performance: Efficient with a small memory footprint and support for async-calls.
Use Cases: Suitable for engineers, scientists, web developers, software teams, and beginners.
Usage: Great for quickly prototyping demos, building internal tools, and sharing knowledge through web apps.