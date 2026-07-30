import { test as setup, expect } from '@playwright/test';
import * as path from 'path';
import * as fs from 'fs';

const AUTH_FILE = path.join(__dirname, '../.auth/admin.json');

setup('authenticate as admin', async ({ page }) => {

  // 1. فحص مجرد وجود الملف + التحقق من صلاحيته
  if (fs.existsSync(AUTH_FILE)) {
    try {
      // نتحقق من تاريخ تعديل الملف: إذا مر عليه أكثر من 8 ساعات مثلاً نحذفه ونجدده تلقائياً
      const stats = fs.statSync(AUTH_FILE);
      const hoursOld = (Date.now() - stats.mtimeMs) / (1000 * 60 * 60);

      if (hoursOld > 8) { // يمكنك تعديل عدد الساعات حسب سياسة الـ Token في موقعك
        console.log('⚠️ Auth file is older than 8 hours — deleting to refresh session...');
        fs.unlinkSync(AUTH_FILE);
      } else {
        console.log('✅ Auth file exists and is fresh — skipping login');
        return;
      }
    } catch {
      // في حال حدوث أي خطأ في قراءة الملف، نحذفه للاحتياط
      if (fs.existsSync(AUTH_FILE)) fs.unlinkSync(AUTH_FILE);
    }
  }

  const email = process.env.ADMIN_EMAIL;
  const password = process.env.ADMIN_PASSWORD;

  if (!email || !password) {
    throw new Error('❌ Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env file!');
  }

  console.log('🚀 Executing fresh login...');
  await page.goto('/login', { waitUntil: 'commit', timeout: 30_000 });

  // خطوة تسجيل الدخول
  const getStartedBtn = page.getByRole('button', { name: 'Get started' });
  await expect(getStartedBtn).toBeVisible({ timeout: 20_000 });
  await getStartedBtn.click();

  const usernameInput = page.getByRole('textbox', { name: 'Email or Username' });
  const passwordInput = page.locator('input[type="password"]');

  await expect(usernameInput).toBeVisible({ timeout: 15_000 });
  await usernameInput.fill(email);
  await passwordInput.fill(password);

  await page.getByRole('button', { name: 'Log In' }).click();

  // التأكد الصريح من التوجيه التام بعيداً عن الـ Login
  await expect(page).not.toHaveURL(/.*login/i, { timeout: 30_000 });

  // حفظ الجلسة الجديدة
  fs.mkdirSync(path.dirname(AUTH_FILE), { recursive: true });
  await page.context().storageState({ path: AUTH_FILE });

  console.log('✅ Fresh auth state saved successfully!');
});