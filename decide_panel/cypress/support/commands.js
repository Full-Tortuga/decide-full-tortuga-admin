Cypress.Commands.add("openInitial", () => {
  cy.visit("http://localhost:3000");
});

Cypress.Commands.add("clickOnView", (value) => {
  cy.get("a.p-tabview-nav-link").contains(value).click();
});

Cypress.Commands.add("closeInLive", () => {
  cy.clickOnView("Prueba de conexión");
});
