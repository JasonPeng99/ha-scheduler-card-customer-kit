const fs = require("fs");
const vm = require("vm");
const path = require("path");

function makeNode() {
  return {
    style: {},
    content: { firstChild: { remove() {}, childNodes: [] }, append() {}, appendChild() {} },
    append() {},
    appendChild() {},
    removeChild() {},
    remove() {},
    setAttribute() {},
    removeAttribute() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent() {
      return true;
    },
    querySelector() {
      return null;
    },
    querySelectorAll() {
      return [];
    },
    attachShadow() {
      return this;
    },
    firstChild: null,
    nextSibling: null,
    parentNode: {
      insertBefore() {
        return makeNode();
      },
    },
    insertBefore() {
      return makeNode();
    },
    getBoundingClientRect() {
      return { width: 100, height: 100, left: 0 };
    },
    blur() {},
    click() {},
  };
}

class StubHTMLElement {
  constructor() {
    this.shadowRoot = null;
  }
  attachShadow() {
    this.shadowRoot = makeNode();
    return this.shadowRoot;
  }
  setAttribute() {}
  removeAttribute() {}
  addEventListener() {}
  removeEventListener() {}
  dispatchEvent() {
    return true;
  }
  append() {}
  appendChild() {}
  removeChild() {}
  querySelector() {
    return null;
  }
  querySelectorAll() {
    return [];
  }
  getAttribute() {
    return null;
  }
}

function buildContext() {
  const customElements = {
    defs: new Map(),
    define(name, klass) {
      this.defs.set(name, klass);
    },
    get(name) {
      return this.defs.get(name);
    },
    whenDefined() {
      return Promise.resolve();
    },
  };

  const documentObj = {
    createElement(tag) {
      const node = makeNode();
      node.tagName = String(tag).toUpperCase();
      node.innerHTML = "";
      return node;
    },
    createComment() {
      return makeNode();
    },
    createTreeWalker() {
      return {
        currentNode: null,
        nextNode() {
          return null;
        },
      };
    },
    importNode(node) {
      return node;
    },
    querySelector() {
      return makeNode();
    },
    querySelectorAll() {
      return [];
    },
    body: makeNode(),
    adoptedStyleSheets: [],
  };

  const context = {
    console,
    setTimeout,
    clearTimeout,
    setInterval,
    clearInterval,
    Promise,
    Map,
    Set,
    WeakMap,
    WeakSet,
    Array,
    Object,
    String,
    Number,
    Boolean,
    Symbol,
    Date,
    Math,
    JSON,
    RegExp,
    URL,
    URLSearchParams,
    HTMLElement: StubHTMLElement,
    customElements,
    Event: class {
      constructor(type, opts) {
        this.type = type;
        Object.assign(this, opts || {});
      }
    },
    CustomEvent: class {
      constructor(type, opts) {
        this.type = type;
        this.detail = opts?.detail;
      }
    },
    DOMParser: class {
      parseFromString() {
        return { body: { textContent: "" } };
      }
    },
    ResizeObserver: class {
      observe() {}
      disconnect() {}
    },
    CSSStyleSheet: class {
      replaceSync() {}
    },
    ShadowRoot: class {},
    Document: class {},
    document: documentObj,
    window: {},
    globalThis: {},
  };

  context.window = context;
  context.globalThis = context;
  return context;
}

function main() {
  const bundlePath = process.argv[2] || path.join(__dirname, "..", "gs-scheduler-card.js");
  const expectedTag = process.argv[3] || "gs-scheduler-card";
  const code = fs.readFileSync(bundlePath, "utf8");

  const context = buildContext();
  vm.createContext(context);
  vm.runInContext(code, context, { timeout: 5000 });

  if (!context.customElements.get(expectedTag)) {
    throw new Error(`Custom element ${expectedTag} was not registered`);
  }

  console.log(`Bundle OK: ${expectedTag} registered from ${bundlePath}`);
}

main();
