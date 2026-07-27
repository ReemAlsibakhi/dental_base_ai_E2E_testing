import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  const email = process.env.ADMIN_EMAIL ?? 'reem_user';
  const password = process.env.ADMIN_PASSWORD ?? 'FaRe12345!!';
  const baseURL = process.env.BASE_URL ?? 'https://dentalbase-dev-v2.vercel.app';

  // Reuse existing auth if still valid
  if (fs.existsSync(AUTH_FILE)) {
    const state = JSON.parse(fs.readFileSync(AUTH_FILE, 'utf-8'));
    if (state?.cookies?.length > 0) {
      await page.context().addCookies(state.cookies);
      await page.goto(`${baseURL}/settings`);
      await page.waitForTimeout(2000);
      if (page.url().includes('/settings')) {
        console.log('Reusing existing auth state');
        return;
      }
    }
  }

  // Fresh login via Keycloak SSO
  await page.goto(`${baseURL}/settings`);
  await page.waitForTimeout(2000);

  // Fill login form
  await page.fill('input[name="username"], input[type="text"]', email);
  await page.fill('input[name="password"], input[type="password"]', password);
  await page.click('button[type="submit"], input[type="submit"]');

  // Wait for redirect back to app
  await page.waitForURL(`${baseURL}/settings**`, { timeout: 30_000 });
  await expect(page.locator('text=Profile').or(page.locator('text=Settings'))).toBeVisible();

  // Save auth state
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('Auth state saved');
});
