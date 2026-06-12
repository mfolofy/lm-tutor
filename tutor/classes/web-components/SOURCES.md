# SOURCES — web-components (Web Components)

## Primary standards

- **WHATWG HTML Living Standard** — Custom Elements, Shadow DOM, Templates, Slots.
  <https://html.spec.whatwg.org/multipage/custom-elements.html>
- **MDN Web Docs — Web Components**. <https://developer.mozilla.org/en-US/docs/Web/API/Web_components>
- **GitHub Catalyst docs**. <https://github.github.io/catalyst/>
- **Lit docs**. <https://lit.dev/>
- **WAI-ARIA 1.2** — Accessibility for shadow DOM. <https://www.w3.org/TR/wai-aria-1.2/>

## Rule-to-standard map

| Rule ID | Primary Source |
|---------|---------------|
| `div-framework-component` | WHATWG HTML — Custom Elements |
| `no-shadow-dom-encapsulation` | WHATWG HTML — Shadow DOM |
| `no-slots` / `named-slots-missing` | WHATWG HTML — slot element |
| `no-css-parts` | CSS Shadow Parts (MDN) |
| `no-form-participation` | WHATWG HTML — Form-associated custom elements |
| `no-declarative-shadow-dom` | WHATWG HTML — Declarative Shadow DOM |
| `catalyst-no-observe` | GitHub Catalyst docs |
| `no-aria-in-shadow` | WAI-ARIA 1.2, MDN |
| `no-elem-internals` | WHATWG HTML — ElementInternals |
| `custom-element-no-lifecycle` | WHATWG HTML — Custom Element lifecycle |
| `inline-styles-global-leak` | WHATWG HTML — Shadow DOM style encapsulation |

## Coverage: ~42% Layer 1, ~58% teaching-only. Verified in tests/test_web_components.py.
