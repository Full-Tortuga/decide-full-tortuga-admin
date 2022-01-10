describe("Initial view of the system", () => {
  beforeEach(() => {
    cy.openInitial();
  });

  it("frontpage can be opened", () => {
    cy.contains("Votaciones");
    cy.closeInLive();
  });

  it("vote section exists", () => {
    cy.contains("Votos");
    cy.closeInLive();  
  });

  it("statistics section exists", () => {
    cy.contains("Estadísticas");
    cy.closeInLive();
  });

  it("backups section exists", () => {
    cy.contains("Backups");
    cy.closeInLive();
  });

  it("connection section exists", () => {
    cy.contains("Prueba de conexión");
    cy.closeInLive();
  });
});
