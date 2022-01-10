describe("Connection test", () => {
  beforeEach(() => {
    cy.openInitial();
    cy.clickOnView("Prueba de conexión");
  });

  it("a successful connection must be obtained", () => {
    cy.contains("Conectar con decide (prueba de conexión)").click();
    cy.contains("Conexión exitosa");
  });
});
