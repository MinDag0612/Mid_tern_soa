const form = document.querySelector('#login-form');
const feedbackEl = document.querySelector('#feedback');

const API_BASE_URL = window.env?.API_BASE_URL ?? 'http://localhost:8000';

const resetFeedback = () => {
  if (feedbackEl) {
    feedbackEl.classList.add('hidden');
  }
};

const showMessage = (message, type = 'success') => {
  if (!feedbackEl) {
    return;
  }
  feedbackEl.textContent = message;
  feedbackEl.className = `feedback ${type}`;
  feedbackEl.classList.remove('hidden');
};

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  resetFeedback();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  try {
    const response = await fetch(`${API_BASE_URL}/accounts/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok || data?.message) {
      showMessage(data.message ?? 'Đăng nhập thất bại', 'error');
      return;
    }

    window.location.href = '/home';
  } catch (error) {
    console.error('Login error', error);
    showMessage('Không thể kết nối máy chủ. Vui lòng thử lại.', 'error');
  }
});
