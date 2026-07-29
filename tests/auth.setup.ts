import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {
  // 1. التخطي إذا كانت الجلسة محفوظة مسبقاً
  if (fs.existsSync(AUTH_FILE)) {
    console.log('✅ Auth file exists — skipping login');
    return;
  }

  const email = process.env.ADMIN_EMAIL;
  const password = process.env.ADMIN_PASSWORD;

  if (!email || !password) {
    throw new Error('❌ Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env file!');
  }

  console.log('🚀 Navigating to login page...');
  await page.goto('/login', { waitUntil: 'commit', timeout: 30_000 });

  // 2. الضغط الصريح على زر Get started (الذي يفتح الفورم)
  const getStartedBtn = page.getByRole('button', { name: 'Get started' });
  console.log('🔹 Waiting for "Get started" button...');
  
  // ننتظر ظهور الزر حتى 20 ثانية لتجاوز بطء تحميل الـ SPA
  await expect(getStartedBtn).toBeVisible({ timeout: 20_000 });
  await getStartedBtn.click();
  console.log('✅ Clicked "Get started"');

  // 3. تحديد الحقول حسب الـ Codegen الصريح
  const usernameInput = page.getByRole('textbox', { name: 'Email or Username' });
  const passwordInput = page.locator('input[type="password"]');

  // 4. تعبئة البيانات بعد ضمان فتح الـ Form
  console.log('🔹 Filling login credentials...');
  await expect(usernameInput).toBeVisible({ timeout: 15_000 });
  await usernameInput.fill(email);

  await expect(passwordInput).toBeVisible({ timeout: 10_000 });
  await passwordInput.fill(password);

  // 5. ضغط زر تسجيل الدخول Log In
  console.log('🔹 Submitting form...');
  await page.getByRole('button', { name: 'Log In' }).click();

  // 6. التحقق وحفظ الجلسة
  console.log('🔹 Verifying authentication...');
  await expect(page).not.toHaveURL(/.*login/i, { timeout: 30_000 });

  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });

  console.log('✅ Auth state saved successfully!');
});