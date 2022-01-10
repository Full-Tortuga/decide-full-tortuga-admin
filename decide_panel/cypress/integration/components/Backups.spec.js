Cypress.config("defaultCommandTimeout", 20000);
describe("Backup generation", () => {
  beforeEach(() => {
    cy.openInitial();
    cy.clickOnView("Backups");
  });

  after(() => {
    cy.closeInLive();
  });

  it("backups page can be opened", () => {
    cy.contains("Generar nuevo backup");
    cy.contains("Activar automatización de backup");
    cy.contains("Desactivar automatización de backup");
  });

  it("backups can be generated", () => {
    cy.contains("Generar nuevo backup").click();
    cy.contains("Se ha creado correctamente el backup");
  });
  
  it("backups aumotatitations can be deactivate", () => {
    cy.contains("Desactivar automatización de backup").click();
    cy.contains("Se ha desactivado la creación automática de backups");
  });

  it("backups aumotatitations can be activate", () => {
    cy.contains("Desactivar automatización de backup").click();
    cy.contains("Activar automatización de backup").click();
    cy.contains("Se ha activado la creación automática de backups");
  });

  it("dropdown to restore backup exists and is clickable", () => {
    cy.get(".p-dropdown-trigger-icon").click();
  });

  it("dropdown to restore backup has a restore option", () => {
    cy.get(".p-dropdown-trigger-icon").click();
    cy.get(".p-dropdown-item").first().click();
    cy.contains("Se ha restaurado correctamente el backup");
  });
});
