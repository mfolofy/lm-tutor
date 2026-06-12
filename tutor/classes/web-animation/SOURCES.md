# SOURCES — web-animation (Web Animation & Motion Design)

## Primary standards

- **CSS Scroll-driven Animations Level 1** (W3C WD). <https://www.w3.org/TR/scroll-animations-1/>
- **CSS View Transitions Level 1** (W3C CR). <https://www.w3.org/TR/css-view-transitions-1/>
- **WCAG 2.2 SC 2.3.3 — Animation from Interactions**. <https://www.w3.org/TR/WCAG22/#animation-from-interactions>
- **Framer Motion docs**. <https://www.framer.com/motion/>
- **GSAP docs**. <https://gsap.com/docs/>
- **Motion One docs**. <https://motion.dev/>
- **Lottie docs**. <https://airbnb.io/lottie/>
- **MDN — Web Animations API**. <https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API>

## Rule-to-standard map

| Rule ID | Primary Source |
|---------|---------------|
| `js-scroll-animation` | CSS Scroll-driven Animations Level 1 |
| `no-prefers-reduced-motion` | WCAG 2.2 SC 2.3.3 |
| `layout-thrashing-animation` | web.dev — animations guide, MDN |
| `no-will-change` | MDN — will-change |
| `giant-gsap-bundle` | GSAP docs — installation |
| `no-compositor-only` | web.dev — animating compositor properties |
| `no-lottie-alt` | Lottie docs — accessibility, WCAG 1.1.1 |
| `animation-duration-too-long` | Material Design — motion duration |
| `no-stagger-delay` | Framer Motion — staggerChildren |
| `no-exit-animation` | Framer Motion — AnimatePresence |
| `infinite-animation-no-pause` | WCAG 2.2 SC 2.3.3, MDN |
| `opacity-zero-hidden` | WCAG 2.4.3 Focus Order, MDN |

## Coverage: ~50% Layer 1, ~50% teaching-only. Verified in tests/test_web_animation.py.
