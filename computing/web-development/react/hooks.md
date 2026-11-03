# Hooks

**Hooks** allow React components to use state and lifecycle features without classes.

**Common Hooks:**

- `useState`: Manage local state.
- `useEffect`: Side effects (API calls, DOM updates).
- `useContext`: Access global context.
- `useMemo`, `useCallback`: Performance optimization.

```jsx
import React, { useState, useEffect } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  useEffect(() => (document.title = `Count: ${count}`));
  return <button onClick={() => setCount(count + 1)}>+1</button>;
}
```
