describe("Votes information", () => {
    beforeEach(() => {
      cy.openInitial();
      cy.clickOnView("Votos");
    });
  
    after(() => {
      cy.closeInLive();
    });
  
    it("the votes result table is displayed", () => {
      cy.get("div.p-datatable-header").contains("Votaciones");
    });
  
    it("all columns are displayed correctly", () => {
      cy.get("span.p-column-title").contains("Votación");
      cy.get("span.p-column-title").contains("Pregunta");
      cy.get("span.p-column-title").contains("Descripción");
      cy.get("span.p-column-title").contains("Fecha Inicio");
      cy.get("span.p-column-title").contains("Fecha Final");
      cy.get("span.p-column-title").contains("Resultado de la Votación");
    });
  });