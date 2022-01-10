describe("System navigation", () => {
  beforeEach(() => {
    cy.openInitial();
  });

  it("the voting page must be displayed", () => {
    cy.clickOnView("Votaciones");
  });

  it("the votes page must be displayed", () => {
    cy.clickOnView("Votos");
  });

  it("the statistics page must be displayed", () => {
    cy.clickOnView("Estadísticas");
  });

  it("the backups page must be displayed", () => {
    cy.clickOnView("Backups");
  });

  it("the connection test page must be displayed", () => {
    cy.clickOnView("Prueba de conexión");
  });
});
