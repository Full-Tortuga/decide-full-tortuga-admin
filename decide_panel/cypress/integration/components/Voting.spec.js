describe("Voting information", () => {
  beforeEach(() => {
    cy.openInitial();
  });

  after(() => {
    cy.closeInLive();
  });

  it("the voting table is displayed", () => {
    cy.get("div.p-datatable-header").contains("Votaciones");
  });

  it("all columns are displayed correctly", () => {
    cy.get("span.p-column-title").contains("Id del votante");
    cy.get("span.p-column-title").contains("Nombre de usuario");
    cy.get("span.p-column-title").contains(new RegExp("^Nombre$", "g"));
    cy.get("span.p-column-title").contains("Apellidos");
    cy.get("span.p-column-title").contains("Email");
    cy.get("span.p-column-title").contains("Género");
    cy.get("span.p-column-title").contains("Región");
    cy.get("span.p-column-title").contains("Id de la votación");
  });
});
