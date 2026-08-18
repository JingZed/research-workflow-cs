# Focused Figure QA

Inspect the actual render at its intended insertion size. Record only the
checks that decide whether this build is usable.

1. Required content and locked wording are present; forbidden or stronger
   claims are absent.
2. Text remains legible, contained, and clearly associated with the intended
   cards, arrows, icons, or regions.
3. Reading order and connector semantics match the scientific relation rather
   than resembling implementation wiring.
4. Aspect ratio, placement, and figure-versus-caption split match the spec or
   explicit request.
5. When a reference is in scope, the render preserves or improves the named
   visual traits appropriate to that reference role.
6. Major icons or visual assets are useful and readable; remove decorative
   placeholders that carry no meaning.

Use `ready` only when these focused checks pass. Otherwise name one concrete
blocker and make at most one bounded correction pass. Do not require a critic,
gate result, reviewer vote, candidate matrix, or next-owner field.
