<template>
  <div class="user-profile-container">
    <div class="user-profile">
      <div class="profile-header">
        <div class="avatar-section">
          <div class="user-avatar large">
            {{ user?.name?.charAt(0) || 'U' }}
          </div>
          <div class="status-indicator" :class="userStatus">
            <span class="status-dot"></span>
            {{ userStatus === 'active' ? 'Активен' : 'Неактивен' }}
          </div>
        </div>
        <div class="header-actions">
          <button 
            v-if="!isEditing" 
            @click="startEditing" 
            class="edit-btn"
          >
            ✏️ Редактировать
          </button>
          <div v-if="isEditing" class="edit-actions">
            <button @click="saveChanges" class="save-btn" :disabled="saving">
              {{ saving ? 'Сохранение...' : '💾 Сохранить' }}
            </button>
            <button @click="cancelEditing" class="cancel-btn">
              ❌ Отменить
            </button>
          </div>
        </div>
      </div>

      <!-- Основная информация -->
      <div class="profile-content">
        <div class="info-section">
          <h3>Основная информация</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>ФИО:</label>
              <input 
                v-if="isEditing" 
                v-model="editForm.name" 
                type="text" 
                class="edit-input"
                placeholder="Введите ФИО"
              />
              <span v-else class="info-value">{{ user?.name || 'Не указано' }}</span>
            </div>

            <div class="info-item">
              <label>Email:</label>
              <input 
                v-if="isEditing" 
                v-model="editForm.email" 
                type="email" 
                class="edit-input"
                placeholder="Введите email"
              />
              <span v-else class="info-value">{{ user?.email || 'Не указано' }}</span>
            </div>

            <div class="info-item">
              <label>Должность:</label>
              <select 
                v-if="isEditing" 
                v-model="editForm.role" 
                class="edit-select"
              >
                <option value="employee">Сотрудник</option>
                <option value="manager">Менеджер</option>
                <option value="admin">Администратор</option>
              </select>
              <span v-else class="info-value role-badge" :class="user?.role">
                {{ getRoleDisplayName(user?.role) }}
              </span>
            </div>

            <div class="info-item">
              <label>Отдел:</label>
              <select 
                v-if="isEditing" 
                v-model="editForm.department" 
                class="edit-select"
              >
                <option value="">Выберите отдел</option>
                <option v-for="dept in departments" :key="dept" :value="dept">
                  {{ dept }}
                </option>
              </select>
              <span v-else class="info-value">{{ user?.department || 'Не указано' }}</span>
            </div>

            <div class="info-item">
              <label>Дата регистрации:</label>
              <span class="info-value">{{ formatDate(user?.created_at) }}</span>
            </div>

            <div class="info-item">
              <label>Последнее обновление:</label>
              <span class="info-value">{{ formatDate(user?.updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Статистика активности -->
        <div class="stats-section">
          <h3>Статистика активности</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-content">
                <h4>Сегодня</h4>
                <p class="stat-value">{{ todayStats.workTime }}</p>
                <span class="stat-label">Время работы</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">📅</div>
              <div class="stat-content">
                <h4>Эта неделя</h4>
                <p class="stat-value">{{ weekStats.workTime }}</p>
                <span class="stat-label">Общее время</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-content">
                <h4>Продуктивность</h4>
                <p class="stat-value">{{ weekStats.productivity }}%</p>
                <span class="stat-label">Средняя за неделю</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">🏆</div>
              <div class="stat-content">
                <h4>Рейтинг</h4>
                <p class="stat-value">#{{ userRating }}</p>
                <span class="stat-label">В отделе</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Последние активности -->
        <div class="activity-section">
          <h3>Последние активности</h3>
          <div class="activity-list">
            <div 
              v-for="activity in recentActivities" 
              :key="activity.id" 
              class="activity-item"
            >
              <div class="activity-icon">
                {{ getActivityIcon(activity.type) }}
              </div>
              <div class="activity-details">
                <h4>{{ activity.title }}</h4>
                <p>{{ activity.description }}</p>
                <span class="activity-time">{{ formatRelativeTime(activity.timestamp) }}</span>
              </div>
              <div class="activity-duration">
                {{ activity.duration }}
              </div>
            </div>
          </div>
        </div>

        <!-- Настройки уведомлений -->
        <div class="settings-section">
          <h3>Настройки</h3>
          <div class="settings-grid">
            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="settings.emailNotifications"
                  @change="updateSettings"
                />
                <span class="checkmark"></span>
                Email уведомления
              </label>
              <p class="setting-description">Получать уведомления о важных событиях</p>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="settings.activityTracking"
                  @change="updateSettings"
                />
                <span class="checkmark"></span>
                Отслеживание активности
              </label>
              <p class="setting-description">Автоматическое отслеживание рабочего времени</p>
            </div>

            <div class="setting-item">
              <label class="setting-label">
                <input 
                  type="checkbox" 
                  v-model="settings.weeklyReports"
                  @change="updateSettings"
                />
                <span class="checkmark"></span>
                Еженедельные отчеты
              </label>
              <p class="setting-description">Получать сводку активности каждую неделю</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Сообщения об ошибках/успехе -->
      <div v-if="message" class="message" :class="messageType">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

// Данные пользователя
const user = computed(() => store.getters['auth/currentUser'])
const userStatus = ref('active') // В реальном приложении получать с сервера

// Состояние редактирования
const isEditing = ref(false)
const saving = ref(false)
const message = ref('')
const messageType = ref('success')

// Форма редактирования
const editForm = reactive({
  name: '',
  email: '',
  role: '',
  department: ''
})

// Настройки
const settings = reactive({
  emailNotifications: true,
  activityTracking: true,
  weeklyReports: false
})

// Справочные данные
const departments = [
  'Разработка',
  'Дизайн', 
  'Маркетинг',
  'Продажи',
  'HR',
  'Финансы',
  'Управление'
]

// Демонстрационные данные статистики
const todayStats = ref({
  workTime: '6ч 45м',
  productivity: 87
})

const weekStats = ref({
  workTime: '32ч 15м',
  productivity: 84
})

const userRating = ref(3)

// Последние активности (демонстрационные данные)
const recentActivities = ref([
  {
    id: 1,
    type: 'work',
    title: 'Работа в VS Code',
    description: 'Разработка нового функционала',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 часа назад
    duration: '2ч 15м'
  },
  {
    id: 2,
    type: 'meeting',
    title: 'Встреча команды',
    description: 'Планирование спринта',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 часа назад
    duration: '1ч 30м'
  },
  {
    id: 3,
    type: 'break',
    title: 'Перерыв',
    description: 'Обеденный перерыв',
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 часов назад
    duration: '45м'
  }
])

// Методы
const getRoleDisplayName = (role) => {
  const roleNames = {
    'admin': 'Администратор',
    'manager': 'Менеджер',
    'employee': 'Сотрудник'
  }
  return roleNames[role] || 'Не указано'
}

const getActivityIcon = (type) => {
  const icons = {
    'work': '💻',
    'meeting': '👥',
    'break': '☕'
  }
  return icons[type] || '📋'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не указано'
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatRelativeTime = (date) => {
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (hours > 0) {
    return `${hours}ч ${minutes}м назад`
  }
  return `${minutes}м назад`
}

const startEditing = () => {
  isEditing.value = true
  // Заполняем форму текущими данными
  editForm.name = user.value?.name || ''
  editForm.email = user.value?.email || ''
  editForm.role = user.value?.role || 'employee'
  editForm.department = user.value?.department || ''
  message.value = ''
}

const cancelEditing = () => {
  isEditing.value = false
  message.value = ''
}

const saveChanges = async () => {
  saving.value = true
  message.value = ''
  
  try {
    // Валидация
    if (!editForm.name.trim()) {
      throw new Error('ФИО обязательно для заполнения')
    }
    if (!editForm.email.trim()) {
      throw new Error('Email обязателен для заполнения')
    }
    if (!editForm.department) {
      throw new Error('Выберите отдел')
    }

    // Имитация API запроса
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Обновляем данные в store
    const updatedUser = {
      ...user.value,
      name: editForm.name,
      email: editForm.email,
      role: editForm.role,
      department: editForm.department,
      updated_at: new Date().toISOString()
    }
    
    store.commit('auth/SET_USER', updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
    
    isEditing.value = false
    message.value = 'Профиль успешно обновлен!'
    messageType.value = 'success'
    
    // Скрываем сообщение через 3 секунды
    setTimeout(() => {
      message.value = ''
    }, 3000)
    
  } catch (error) {
    message.value = error.message || 'Ошибка при сохранении изменений'
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

const updateSettings = () => {
  // Сохранение настроек в localStorage или отправка на сервер
  localStorage.setItem('userSettings', JSON.stringify(settings))
  
  message.value = 'Настройки сохранены'
  messageType.value = 'success'
  
  setTimeout(() => {
    message.value = ''
  }, 2000)
}

onMounted(() => {
  // Загружаем сохраненные настройки
  const savedSettings = localStorage.getItem('userSettings')
  if (savedSettings) {
    Object.assign(settings, JSON.parse(savedSettings))
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&display=swap');

.user-profile-container {
  font-family: 'Gabarito', sans-serif;
  color: rgba(243, 238, 232, 1);
  max-width: 1000px;
  margin: 0 auto;
}

.user-profile {
  background: rgba(19, 24, 27, 1);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(243, 238, 232, 0.1);
}

/* Заголовок профиля */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(243, 238, 232, 0.2);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(131, 21, 21, 1), rgba(151, 31, 31, 1));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 32px;
  color: rgba(243, 238, 232, 1);
  box-shadow: 0 4px 12px rgba(131, 21, 21, 0.3);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

.status-indicator.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.status-indicator.inactive {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-family: 'Gabarito', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: rgba(33, 150, 243, 1);
  color: white;
}

.edit-btn:hover {
  background: rgba(25, 118, 210, 1);
  transform: translateY(-2px);
}

.save-btn {
  background: rgba(76, 175, 80, 1);
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: rgba(69, 160, 73, 1);
  transform: translateY(-2px);
}

.save-btn:disabled {
  background: rgba(76, 175, 80, 0.5);
  cursor: not-allowed;
}

.cancel-btn {
  background: rgba(131, 21, 21, 1);
  color: white;
}

.cancel-btn:hover {
  background: rgba(151, 31, 31, 1);
  transform: translateY(-2px);
}

.edit-actions {
  display: flex;
  gap: 10px;
}

/* Основной контент */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.info-section h3,
.stats-section h3,
.activity-section h3,
.settings-section h3 {
  margin: 0 0 20px 0;
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
  font-size: 20px;
}

/* Информационная секция */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item label {
  font-weight: 600;
  color: rgba(243, 238, 232, 0.8);
  font-size: 14px;
}

.info-value {
  font-size: 16px;
  color: rgba(243, 238, 232, 1);
  font-weight: 500;
}

.role-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.role-badge.admin {
  background: rgba(156, 39, 176, 0.2);
  color: #9C27B0;
}

.role-badge.manager {
  background: rgba(255, 152, 0, 0.2);
  color: #FF9800;
}

.role-badge.employee {
  background: rgba(33, 150, 243, 0.2);
  color: #2196F3;
}

.edit-input,
.edit-select {
  padding: 10px 15px;
  border: 1px solid rgba(243, 238, 232, 0.3);
  border-radius: 8px;
  background: rgba(58, 60, 65, 1);
  color: rgba(243, 238, 232, 1);
  font-family: 'Gabarito', sans-serif;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.edit-input:focus,
.edit-select:focus {
  outline: none;
  border-color: rgba(33, 150, 243, 1);
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

/* Статистика */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.stat-icon {
  font-size: 2rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h4 {
  margin: 0 0 5px 0;
  font-size: 14px;
  color: rgba(243, 238, 232, 0.8);
  font-weight: 500;
}

.stat-value {
  margin: 0 0 5px 0;
  font-size: 20px;
  font-weight: 700;
  color: rgba(243, 238, 232, 1);
}

.stat-label {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
}

/* Активности */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.3s ease;
}

.activity-item:hover {
  transform: translateX(5px);
}

.activity-icon {
  font-size: 1.5rem;
  background: rgba(131, 21, 21, 0.2);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-details {
  flex: 1;
}

.activity-details h4 {
  margin: 0 0 5px 0;
  font-weight: 600;
  font-size: 16px;
}

.activity-details p {
  margin: 0 0 5px 0;
  color: rgba(243, 238, 232, 0.8);
  font-size: 14px;
}

.activity-time {
  font-size: 12px;
  color: rgba(243, 238, 232, 0.6);
}

.activity-duration {
  font-weight: 600;
  color: rgba(243, 238, 232, 1);
}

/* Настройки */
.settings-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setting-item {
  background: rgba(58, 60, 65, 1);
  border-radius: 12px;
  padding: 20px;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 8px;
}

.setting-label input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(243, 238, 232, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.setting-label input[type="checkbox"]:checked + .checkmark {
  background: rgba(76, 175, 80, 1);
  border-color: rgba(76, 175, 80, 1);
}

.setting-label input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 12px;
}

.setting-description {
  margin: 0;
  color: rgba(243, 238, 232, 0.7);
  font-size: 14px;
}

/* Сообщения */
.message {
  margin-top: 20px;
  padding: 15px 20px;
  border-radius: 8px;
  font-weight: 600;
  text-align: center;
}

.message.success {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.message.error {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

/* Адаптивность */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
  }

  .avatar-section {
    justify-content: center;
  }

  .header-actions {
    justify-content: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .activity-item {
    flex-direction: column;
    text-align: center;
  }

  .edit-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .user-profile {
    padding: 20px;
  }
}
</style>