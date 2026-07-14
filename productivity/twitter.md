# Twitter

## Unlike All Likes

1. Open Chrome or Firefox.
2. Log in to your [Twitter Likes page](https://twitter.com/your_username/likes).
3. Open your browser’s Developer Tools:
   - Windows/Linux: `F12` or `Ctrl+Shift+I`
   - macOS: `Cmd+Option+I`
4. Go to the **Console** tab.
5. Paste the following script and press `Enter`.

```javascript
setInterval(() => {
  for (const d of document.querySelectorAll('button[data-testid="unlike"]')) {
    d.click();
  }
  window.scrollTo(0, document.body.scrollHeight);
}, 5000);
```
