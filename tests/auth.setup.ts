import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  if (!process.env.ADMIN_EMAIL || !process.env.ADMIN_PASSWORD) {
    throw new Error('Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env');
  }

  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  await page.goto('/login');

  // Wait indefinitely for "Get started" — no fixed timeout
  // DentalBase load time varies, this is the correct approach for SPAs
  const getStarted = page.getByRole('button', { name: 'Get started' });
  await getStarted.waitFor({ state: 'visible' });
  await getStarted.click();

  await page.getByRole('textbox', { name: 'Email or Username' }).fill(process.env.ADMIN_EMAIL);
  await page.getByRole('textbox', { name: 'Password' }).fill(process.env.ADMIN_PASSWORD);
  await page.getByRole('button', { name: 'Log In' }).click();

  await expect(page).not.toHaveURL(/login/);

  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });
  console.log('✅ Auth state saved');
});
