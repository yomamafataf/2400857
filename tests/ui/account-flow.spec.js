const {test, expect} = require("@playwright/test");

test("rejects a short password on the account page", async ({page}) => {
  await page.goto("/");
  await page.getByLabel("Username").fill("ui-short-test");
  await page.getByLabel("Password").fill("short");
  await page.getByRole("button", {name: /create account/i}).click();
  await expect(page.getByRole("alert")).toContainText("at least 10 characters");
  await expect(page.getByRole("heading", {name: "Create account"})).toBeVisible();
});

test("rejects a password from the database blocklist", async ({page}) => {
  await page.goto("/");
  await page.getByLabel("Username").fill("ui-common-test");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", {name: /create account/i}).click();
  await expect(page.getByRole("alert")).toContainText("common-password blocklist");
});

test("creates an account, displays the password, and logs out", async ({page}) => {
  const password = "UI passphrase 2400857!";
  await page.goto("/");
  await page.getByLabel("Username").fill("ui-success-test");
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", {name: /create account/i}).click();
  await expect(page.getByRole("heading", {name: "Welcome, ui-success-test"})).toBeVisible();
  await expect(page.locator("output")).toHaveText(password);
  await page.getByRole("button", {name: "Log out"}).click();
  await expect(page.getByRole("heading", {name: "Create account"})).toBeVisible();
});
