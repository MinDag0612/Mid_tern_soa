const API_BASE_URL = window.env?.API_BASE_URL ?? 'http://localhost:8000';
const token = localStorage.getItem('access_token');

let userInfor = null;
const rawUserInfor = localStorage.getItem('user_infor');
if (rawUserInfor) {
  try {
    const parsed = JSON.parse(rawUserInfor);
    if (parsed && typeof parsed === 'object') {
      userInfor = parsed;
    }
  } catch (error) {
    console.warn('Không thể parse user_infor từ localStorage', error);
  }
}

if (!userInfor) {
  const fallbackId = localStorage.getItem('customer_id');
  if (fallbackId) {
    userInfor = {
      id: fallbackId,
      fullName: localStorage.getItem('customer_fullname') ?? '',
      email: localStorage.getItem('customer_email') ?? '',
      phoneNumber: localStorage.getItem('customer_phone') ?? '',
      balance: localStorage.getItem('customer_balance'),
    };
  }
}

if (userInfor && typeof userInfor.id === 'string') {
  const numericId = Number.parseInt(userInfor.id, 10);
  if (!Number.isNaN(numericId)) {
    userInfor.id = numericId;
  }
}

if (userInfor && userInfor.balance !== undefined && userInfor.balance !== null) {
  const numericBalance = Number.parseFloat(userInfor.balance);
  if (!Number.isNaN(numericBalance)) {
    userInfor.balance = numericBalance;
  }
}

const hasValidSession = Boolean(token) && userInfor && userInfor.id !== undefined && userInfor.id !== null && `${userInfor.id}` !== '';
if (!hasValidSession) {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_infor');
  localStorage.removeItem('customer_id');
  localStorage.removeItem('customer_fullname');
  localStorage.removeItem('customer_email');
  localStorage.removeItem('customer_phone');
  localStorage.removeItem('customer_balance');
  window.location.replace('/');
}

const popupEl = document.getElementById('popup');
const popupMessageEl = document.getElementById('popup-message');
const popupCloseBtn = document.getElementById('popup-close');

let popupTimer = null;

const clearPopupTimer = () => {
  if (popupTimer) {
    window.clearTimeout(popupTimer);
    popupTimer = null;
  }
};

const hidePopup = () => {
  if (!popupEl) {
    return;
  }
  clearPopupTimer();
  popupEl.classList.add('hidden');
  popupEl.classList.remove('popup--info', 'popup--success', 'popup--error');
  popupEl.setAttribute('aria-hidden', 'true');
};

const showToast = (message, type = 'info') => {
  if (!popupEl || !popupMessageEl) {
    return;
  }

  clearPopupTimer();
  popupMessageEl.textContent = message;
  popupEl.classList.remove('hidden', 'popup--info', 'popup--success', 'popup--error');
  popupEl.classList.add(`popup--${type}`);
  popupEl.setAttribute('aria-hidden', 'false');

  if (type === 'error') {
    window.setTimeout(() => {
      popupCloseBtn?.focus();
    }, 0);
  } else {
    popupTimer = window.setTimeout(() => {
      hidePopup();
    }, 2600);
  }
};

popupCloseBtn?.addEventListener('click', hidePopup);
popupEl?.addEventListener('click', (event) => {
  if (event.target === popupEl) {
    hidePopup();
  }
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && popupEl && !popupEl.classList.contains('hidden')) {
    hidePopup();
  }
});

if (popupEl) {
  popupEl.setAttribute('aria-hidden', popupEl.classList.contains('hidden') ? 'true' : 'false');
}

const sections = document.querySelectorAll('.content');
const menuLinks = document.querySelectorAll('.menu-link');

const DEFAULT_SECTION = 'hocphi';
const SECTION_STORAGE_KEY = 'homepage_active_section';
const TUITION_CACHE_KEY = 'homepage_tuition_cache_v1';
const STUDENT_ID_STORAGE_KEY = 'homepage_student_id';
const CACHE_TTL_MS = 5 * 60 * 1000; // Cache tuition results for 5 minutes

const switchSection = (targetSection) => {
  const desired = Array.from(sections).some((section) => section.id === targetSection)
    ? targetSection
    : DEFAULT_SECTION;

  sections.forEach((section) => {
    section.classList.toggle('hidden', section.id !== desired);
  });

  menuLinks.forEach((item) => {
    item.classList.toggle('active', item.dataset.section === desired);
  });

  try {
    localStorage.setItem(SECTION_STORAGE_KEY, desired);
  } catch (storageError) {
    console.warn('Không thể lưu trạng thái tab đang xem', storageError);
  }

  return desired;
};

menuLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    switchSection(link.dataset.section);
  });
});

const savedSection = localStorage.getItem(SECTION_STORAGE_KEY);
const initialSection = switchSection(savedSection ?? DEFAULT_SECTION);

const profileButton = document.getElementById('profile-button');
const dropdownMenu = document.getElementById('dropdownMenu');

profileButton?.addEventListener('click', () => {
  dropdownMenu?.classList.toggle('show');
});

document.addEventListener('click', (event) => {
  if (!dropdownMenu || !profileButton) {
    return;
  }
  if (event.target === profileButton || profileButton.contains(event.target)) {
    return;
  }
  if (!dropdownMenu.contains(event.target)) {
    dropdownMenu.classList.remove('show');
  }
});

const logoutButton = document.getElementById('logout');
logoutButton?.addEventListener('click', () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_infor');
  localStorage.removeItem('customer_id');
  localStorage.removeItem('customer_fullname');
  localStorage.removeItem('customer_email');
  localStorage.removeItem('customer_phone');
  localStorage.removeItem('customer_balance');
  window.location.href = '/';
});

const profileNameEl = document.getElementById('profile-name');
const profileEmailEl = document.getElementById('profile-email');
const profilePhoneEl = document.getElementById('profile-phone');
const profileIdEl = document.getElementById('profile-id');
const profileBalanceEl = document.getElementById('profile-balance');
const dropdownNameEl = document.getElementById('dropdown-name');
const dropdownEmailEl = document.getElementById('dropdown-email');
const dropdownCustomerEl = document.getElementById('dropdown-customer');

const formatCurrency = (value) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(Number(value ?? 0));

const populateProfile = () => {
  const { fullName, email, phoneNumber, id, balance } = userInfor ?? {};
  profileNameEl.textContent = fullName ?? '—';
  profileEmailEl.textContent = email ?? '—';
  if (profilePhoneEl) {
    profilePhoneEl.textContent = phoneNumber ?? '—';
  }
  profileIdEl.textContent = id ?? '—';
  if (profileBalanceEl) {
    profileBalanceEl.textContent =
      balance !== undefined && balance !== null && !Number.isNaN(Number(balance))
        ? formatCurrency(balance)
        : '—';
  }
  dropdownNameEl.textContent = fullName ?? '—';
  dropdownEmailEl.textContent = email ?? '—';
  dropdownCustomerEl.textContent = `Mã KH: ${id ?? '—'}`;
};

populateProfile();

const lookupForm = document.getElementById('lookup-form');
const studentIdInput = document.getElementById('student-id');
const tuitionEmptyEl = document.getElementById('tuition-empty');
const tuitionTableWrapper = document.getElementById('tuition-table-wrapper');
const tuitionTableBody = document.querySelector('#tuition-table tbody');
const tuitionTemplate = document.getElementById('tuition-row-template');

const otpForm = document.getElementById('otp-form');
const paymentForm = document.getElementById('payment-form');
const otpTransactionInput = document.getElementById('otp-transaction');
const paymentTransactionInput = document.getElementById('payment-transaction');
const paymentOtpInput = document.getElementById('payment-otp');
const historyTableBody = document.querySelector('#history-table tbody');
const historyTableFullBody = document.querySelector('#history-table-full tbody');

let currentStudentId = '';
let paymentHistoryCache = [];
let lastHistoryFetchedAt = 0;
const HISTORY_CACHE_TTL_MS = 2 * 60 * 1000; // 2 minutes

const readTuitionCache = () => {
  const raw = localStorage.getItem(TUITION_CACHE_KEY);
  if (!raw) {
    return {};
  }
  try {
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === 'object') {
      return parsed;
    }
  } catch (error) {
    console.warn('Không thể đọc cache học phí', error);
  }
  return {};
};

const writeTuitionCache = (cache) => {
  try {
    localStorage.setItem(TUITION_CACHE_KEY, JSON.stringify(cache));
  } catch (error) {
    console.warn('Không thể lưu cache học phí', error);
  }
};

const getCachedTuition = (studentId) => {
  if (!studentId) {
    return null;
  }
  const cache = readTuitionCache();
  const entry = cache?.[studentId];
  if (!entry) {
    return null;
  }
  const { records, fetchedAt } = entry;
  if (!Array.isArray(records) || typeof fetchedAt !== 'number') {
    delete cache[studentId];
    writeTuitionCache(cache);
    return null;
  }
  if (Date.now() - fetchedAt > CACHE_TTL_MS) {
    delete cache[studentId];
    writeTuitionCache(cache);
    return null;
  }
  return entry;
};

const setCachedTuition = (studentId, records) => {
  if (!studentId || !Array.isArray(records)) {
    return;
  }
  const cache = readTuitionCache();
  cache[studentId] = {
    records,
    fetchedAt: Date.now(),
  };
  writeTuitionCache(cache);
};

const removeTuitionCache = (studentId) => {
  if (!studentId) {
    return;
  }
  const cache = readTuitionCache();
  if (!cache?.[studentId]) {
    return;
  }
  delete cache[studentId];
  writeTuitionCache(cache);
};

const copyToClipboard = async (value) => {
  if (!value) {
    return;
  }
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }
  const helper = document.createElement('textarea');
  helper.value = value;
  helper.setAttribute('readonly', '');
  helper.style.position = 'fixed';
  helper.style.opacity = '0';
  document.body.appendChild(helper);
  helper.select();
  document.execCommand('copy');
  document.body.removeChild(helper);
};

const renderEmptyState = (message) => {
  tuitionEmptyEl.textContent = message;
  tuitionEmptyEl.classList.remove('hidden');
  tuitionTableWrapper.classList.add('hidden');
  tuitionTableBody.innerHTML = '';
};

const renderTuitionRows = (records) => {
  if (!Array.isArray(records) || records.length === 0) {
    renderEmptyState('Không còn khoản học phí nào cần thanh toán.');
    return;
  }

  tuitionEmptyEl.classList.add('hidden');
  tuitionTableWrapper.classList.remove('hidden');
  tuitionTableBody.innerHTML = '';

  records.forEach((record) => {
    const row = tuitionTemplate.content.firstElementChild.cloneNode(true);

    const transactionCell = row.querySelector('[data-cell="transaction"]');
    transactionCell.textContent = '';
    transactionCell.classList.add('transaction-cell');

    const transactionText = document.createElement('span');
    transactionText.className = 'transaction-code';
    transactionText.textContent = record.idTransaction;
    transactionCell.appendChild(transactionText);

    const copyButton = document.createElement('button');
    copyButton.type = 'button';
    copyButton.className = 'copy-btn';
    copyButton.textContent = 'Sao chép';
    copyButton.addEventListener('click', async () => {
      if (otpTransactionInput) {
        otpTransactionInput.value = record.idTransaction;
      }
      if (paymentTransactionInput) {
        paymentTransactionInput.value = record.idTransaction;
      }
      try {
        await copyToClipboard(record.idTransaction);
        showToast('Đã sao chép mã giao dịch.', 'success');
      } catch (error) {
        console.error('copy transaction error', error);
        showToast('Không thể sao chép mã. Vui lòng thử lại.', 'error');
      }
    });
    transactionCell.appendChild(copyButton);

    row.querySelector('[data-cell="student"]').textContent = `${record.studentName} (${record.studentId})`;
    row.querySelector('[data-cell="amount"]').textContent = formatCurrency(record.tuition);

    const statusBadge = document.createElement('span');
    statusBadge.className = `badge ${record.is_paid ? 'success' : 'warning'}`;
    statusBadge.textContent = record.is_paid ? 'Đã thanh toán' : 'Chưa thanh toán';
    row.querySelector('[data-cell="status"]').appendChild(statusBadge);

    tuitionTableBody.appendChild(row);
  });
};

const renderHistoryRows = (records, targetBody) => {
  if (!targetBody) {
    return;
  }
  targetBody.innerHTML = '';
  if (!Array.isArray(records) || records.length === 0) {
    const emptyRow = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 4;
    cell.className = 'empty-state';
    cell.textContent = 'Chưa có giao dịch nào.';
    emptyRow.appendChild(cell);
    targetBody.appendChild(emptyRow);
    return;
  }

  records.forEach((item) => {
    const row = document.createElement('tr');
    const paidAt = item.paid_at ? new Date(item.paid_at) : null;

    const transactionTd = document.createElement('td');
    transactionTd.textContent = item.transaction_id;
    row.appendChild(transactionTd);

    const studentTd = document.createElement('td');
    const amountTd = document.createElement('td');
    amountTd.textContent = formatCurrency(item.tuition);
    row.appendChild(amountTd);

    const timeTd = document.createElement('td');
    timeTd.textContent = paidAt
      ? paidAt.toLocaleString('vi-VN', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false,
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
        })
      : '—';
    row.appendChild(timeTd);

    const payerTd = document.createElement('td');
    payerTd.textContent = item.payer ?? '—';
    row.appendChild(payerTd);

    targetBody.appendChild(row);
  });
};

const refreshHistoryViews = () => {
  if (historyTableBody) {
    renderHistoryRows(paymentHistoryCache.slice(0, 20), historyTableBody);
  }
  if (historyTableFullBody) {
    renderHistoryRows(paymentHistoryCache, historyTableFullBody);
  }
};

const fetchPaymentHistory = async (force = false) => {
  if (!userInfor?.id) {
    return;
  }
  const now = Date.now();
  if (!force && now - lastHistoryFetchedAt < HISTORY_CACHE_TTL_MS && paymentHistoryCache.length) {
    refreshHistoryViews();
    return;
  }
  try {
    const response = await fetch(
      `${API_BASE_URL}/payment/history?customer_id=${userInfor.id}&limit=50`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    const result = await response.json().catch(() => null);
    if (!response.ok) {
      throw new Error(result?.message ?? 'Không thể tải lịch sử giao dịch.');
    }
    paymentHistoryCache = Array.isArray(result) ? result : [];
    lastHistoryFetchedAt = now;
    refreshHistoryViews();
  } catch (error) {
    console.error('fetch history error', error);
    showToast(error.message ?? 'Không thể tải lịch sử giao dịch.', 'error');
  }
};

const updateStudentInfo = (records) => {
  const firstRecord = Array.isArray(records) ? records[0] : null;
  if (!firstRecord?.studentId) {
    try {
      localStorage.removeItem('homepage_last_student');
    } catch (error) {
      console.warn('Không thể xóa MSSV cuối cùng đã tra cứu', error);
    }
    return;
  }
  try {
    localStorage.setItem('homepage_last_student', firstRecord.studentId);
  } catch (error) {
    console.warn('Không thể lưu MSSV cuối cùng đã tra cứu', error);
  }
};
const fetchTuition = async (studentId) => {
  currentStudentId = studentId;
  try {
    const response = await fetch(`${API_BASE_URL}/tuition/getTuition`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ studentId }),
    });

    const result = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(result?.message ?? 'Không thể tải học phí.');
    }

    if (Array.isArray(result)) {
      updateStudentInfo(result);
      renderTuitionRows(result);
      setCachedTuition(studentId, result);
      try {
        localStorage.setItem(STUDENT_ID_STORAGE_KEY, studentId);
      } catch (storageError) {
        console.warn('Không thể lưu MSSV đã tra cứu', storageError);
      }
      showToast('Đã tải danh sách học phí.', 'success');
      return;
    }

    const message = result?.message ?? 'Không tìm thấy dữ liệu.';
    renderEmptyState(message);
    updateStudentInfo(null);
    removeTuitionCache(studentId);
    try {
      localStorage.setItem(STUDENT_ID_STORAGE_KEY, studentId);
    } catch (storageError) {
      console.warn('Không thể lưu MSSV đã tra cứu', storageError);
    }
    showToast(message, 'info');
  } catch (error) {
    console.error('fetch tuition error', error);
    renderEmptyState('Không thể tải dữ liệu học phí. Vui lòng thử lại.');
    updateStudentInfo(null);
    try {
      localStorage.setItem(STUDENT_ID_STORAGE_KEY, studentId);
    } catch (storageError) {
      console.warn('Không thể lưu MSSV đã tra cứu', storageError);
    }
    showToast(error.message, 'error');
  }
};

const hydrateTuitionFromCache = (activeSection) => {
  if (!studentIdInput) {
    return;
  }

  const savedId = localStorage.getItem(STUDENT_ID_STORAGE_KEY);
  if (savedId) {
    studentIdInput.value = savedId;
  }

  const cachedEntry = getCachedTuition(savedId);
  if (!cachedEntry) {
    return;
  }

  currentStudentId = savedId;
  updateStudentInfo(cachedEntry.records);
  renderTuitionRows(cachedEntry.records);

  if (activeSection !== 'hocphi') {
    return;
  }

  const lastUpdated = new Date(cachedEntry.fetchedAt);
  if (!Number.isNaN(lastUpdated.getTime())) {
    const formatted = lastUpdated.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
    showToast(`Hiển thị dữ liệu lưu lúc ${formatted}.`, 'info');
  } else {
    showToast('Đang hiển thị dữ liệu học phí đã lưu gần đây.', 'info');
  }
};

lookupForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const studentId = studentIdInput.value.trim();
  if (!studentId) {
    showToast('Vui lòng nhập mã số sinh viên.', 'error');
    return;
  }
  fetchTuition(studentId);
});

hydrateTuitionFromCache(initialSection);
if (initialSection === 'thanhtoan' || initialSection === 'lichsu') {
  fetchPaymentHistory(true);
}

const requestOtp = async (transactionId) => {
  try {
    showToast('Đang gửi yêu cầu OTP...', 'info');
    const response = await fetch(`${API_BASE_URL}/otp/request-otp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ transaction_id: transactionId, customer_id: userInfor.id }),
    });
    const result = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(result?.message ?? 'Không thể gửi OTP.');
    }

    showToast(result?.message ?? 'Đã gửi OTP tới email của bạn.', 'success');
  } catch (error) {
    console.error('request otp error', error);
    showToast(error.message, 'error');
  }
};

otpForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const transactionId = otpTransactionInput.value.trim();
  if (!transactionId) {
    showToast('Vui lòng nhập mã giao dịch để yêu cầu OTP.', 'error');
    return;
  }
  paymentTransactionInput.value = transactionId;
  await requestOtp(transactionId);
});

const verifyOtpBeforePayment = async (transactionId, otpCode) => {
  const response = await fetch(`${API_BASE_URL}/otp/verify-otp`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      transaction_id: transactionId,
      otp_input: otpCode,
    }),
  });

  const result = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(result?.message ?? 'OTP không hợp lệ.');
  }

  return result;
};

paymentForm?.addEventListener('submit', async (event) => {
  event.preventDefault();

  const transactionId = paymentTransactionInput.value.trim();
  const otpCode = paymentOtpInput.value.trim();

  if (!transactionId || !otpCode) {
    showToast('Vui lòng nhập đủ mã giao dịch và OTP.', 'error');
    return;
  }

  try {
    try {
      await verifyOtpBeforePayment(transactionId, otpCode);
    } catch (otpError) {
      showToast(otpError.message, 'error');
      return;
    }

    const response = await fetch(`${API_BASE_URL}/payment/pay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        transaction_id: transactionId,
        customer_id: userInfor.id,
        otp_code: otpCode,
      }),
    });

    const result = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(result?.message ?? 'Thanh toán thất bại.');
    }

    paymentForm.reset();
    showToast(result?.message ?? 'Thanh toán thành công.', 'success');

    if (currentStudentId) {
      fetchTuition(currentStudentId);
    }
    fetchPaymentHistory(true);
  } catch (error) {
    console.error('payment error', error);
    showToast(error.message, 'error');
  }
});

// Auto focus student ID chỉ khi đang ở tab Học phí
if (initialSection === 'hocphi') {
  studentIdInput?.focus();
}

menuLinks.forEach((link) => {
  link.addEventListener('click', () => {
    if (link.dataset.section === 'thanhtoan' || link.dataset.section === 'lichsu') {
      fetchPaymentHistory();
    }
  });
});
