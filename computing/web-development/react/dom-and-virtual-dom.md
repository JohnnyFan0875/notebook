# DOM

**DOM (Document Object Model):**

- A tree structure representing HTML elements in a web page.
- Direct DOM manipulation can be slow for frequent updates.

**Virtual DOM:**

- An in-memory representation of the DOM.
- React uses it to calculate the minimal set of changes and update efficiently.
- Benefits: improved performance, cleaner state-driven UI updates.

```js
// Example: Virtual DOM update logic (conceptually)
const newVDOM = render(App());
updateDOM(diff(oldVDOM, newVDOM));
```
