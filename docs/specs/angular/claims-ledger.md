# Angular Lab — claims ledger
Legend: ✅ V verified on angular.dev · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers) · 👤 U from the user.
Source root: https://angular.dev/

## Page 1 — mental model
| Claim | Status | Note |
|---|---|---|
| The object passed to @Component is its metadata: selector, template and more; templates/styles inline or in templateUrl/styleUrl | ✅ V | angular.dev/guide/components |
| By default Angular components are standalone and added directly to other components' imports; before v19 standalone defaulted to false | ✅ V | angular.dev/guide/components; migrations |
| The imports property lists the standalone component's template dependencies (directives, components, pipes) | ✅ V | angular.dev/api/core/Component |
| A component shows by creating an element matching its selector in another component's template | ✅ V | angular.dev/guide/components |
| Interpolation {{ }}; property/attribute binding (attr. prefix for attributes); two-way binding [()] combines [] and () ("banana in a box"); model() creates two-way bindable inputs | ✅ V | guide/templates/binding, two-way-binding |
| [(ngModel)] requires FormsModule | ✅ V | guide/forms/template-driven-forms |
| input() exposes a read-only signal; input.required() for required inputs; output() declares outputs emitted with .emit; model() creates an input and a …Change output | ✅ V | guide/components/inputs; api/core/input, ModelSignal |
| provideHttpClient goes in app.config.ts providers; provideRouter returns environment providers; environment providers cannot go in a component's providers (NG0207) | ✅ V | guide/http/setup; api/router/provideRouter; errors/NG0207 |
| Zoneless is stable (v20.2) and default in v21+; OnPush becoming the default strategy and Default renamed Eager (roadmap); one best-practices page ties OnPush-default to v22 | ✅ V | guide/zoneless; roadmap — version labels differ between pages, readers told to check release notes |
| Error messages (“is not a known element”, “Can't bind to …”) | 🟨 K | Angular's usual compiler messages, wording not re-checked |
| React ↔ Angular vocabulary table | 🟦 I | teaching analogy, not an official mapping |
| ShopUI: 504 components, ≈ 40 ms with the old default strategy; "2019" as the year of an old tutorial | 🟦 I | teaching numbers / example |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
