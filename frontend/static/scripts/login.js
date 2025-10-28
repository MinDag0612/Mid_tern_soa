const form = document.querySelector('#login-form');
const feedbackEl = document.querySelector('#feedback');
const submitBtn = form?.querySelector('button[type="submit"]');

const API_BASE_URL = window.env?.API_BASE_URL ?? 'http://localhost:8000';

const resetFeedback = () => {
  if (feedbackEl) {
    feedbackEl.className = 'feedback hidden';
    feedbackEl.textContent = '';
  }
};

const showMessage = (message, type = 'success') => {
  if (!feedbackEl) {
    return;
  }
  feedbackEl.textContent = message;
  feedbackEl.className = `feedback ${type}`;
};

const setLoadingState = (isLoading) => {
  if (!submitBtn) {
    return;
  }
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? 'Đang kiểm tra…' : 'Đăng nhập';
};

const clearSession = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_infor');
  localStorage.removeItem('customer_id');
  localStorage.removeItem('customer_fullname');
  localStorage.removeItem('customer_email');
};

const persistSession = (result) => {
  const infor = result?.user_infor ?? {};
  localStorage.setItem('access_token', result.access_token);
  try {
    localStorage.setItem('user_infor', JSON.stringify(infor));
  } catch (error) {
    console.warn('Không thể lưu user_infor ở dạng JSON', error);
  }
  if (infor?.id !== undefined) {
    localStorage.setItem('customer_id', String(infor.id));
  }
  if (infor?.fullName !== undefined) {
    localStorage.setItem('customer_fullname', infor.fullName ?? '');
  }
  if (infor?.email !== undefined) {
    localStorage.setItem('customer_email', infor.email ?? '');
  }
};

form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  resetFeedback();
  setLoadingState(true);

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  const payloadToSend = {
    username: payload.user_name ?? payload.username ?? '',
    password: payload.password ?? '',
  };

  try {
    const response = await fetch(`${API_BASE_URL}/accounts/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payloadToSend),
    });

    const result = await response.json().catch(() => null);

    if (!response.ok || !result || result?.message) {
      clearSession();
      showMessage(result?.message ?? 'Đăng nhập thất bại', 'error');
      return;
    }

    persistSession(result);

    window.location.href = '/home';
  } catch (error) {
    console.error('Login error', error);
    clearSession();
    showMessage('Không thể kết nối máy chủ. Vui lòng thử lại.', 'error');
  } finally {
    setLoadingState(false);
  }
});
