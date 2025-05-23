// Personal Data Visualizer - Dashboard JavaScript

class DashboardManager {
  constructor() {
    this.charts = {}
    this.init()
  }

  init() {
    console.log('🎵 Dashboard Manager initialized')
    this.setupEventListeners()
    this.loadAllCharts()
  }

  setupEventListeners() {
    // Refresh button functionality
    const refreshBtn = document.getElementById('refreshData')
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refreshAllData())
    }

    // Chart resize handling
    window.addEventListener('resize', () => {
      Object.values(this.charts).forEach((chart) => {
        if (chart && typeof chart.resize === 'function') {
          chart.resize()
        }
      })
    })
  }

  async loadAllCharts() {
    try {
      await Promise.all([
        this.loadGenresChart(),
        this.loadTimeChart(),
        this.loadAudioFeaturesChart(),
      ])
    } catch (error) {
      console.error('Erro ao carregar gráficos:', error)
      this.showError('Erro ao carregar alguns gráficos')
    }
  }

  async loadGenresChart() {
    try {
      const response = await fetch('/api/charts/genres')
      const data = await response.json()

      if (data.labels && data.values && data.labels.length > 0) {
        this.createPieChart(
          'genresChart',
          data.labels,
          data.values,
          'Distribuição de Gêneros Musicais'
        )
      } else {
        this.showChartPlaceholder(
          'genresChart',
          'Sem dados de gêneros disponíveis'
        )
      }
    } catch (error) {
      console.error('Erro ao carregar gráfico de gêneros:', error)
      this.showChartError('genresChart', 'Erro ao carregar gêneros')
    }
  }

  async loadTimeChart() {
    try {
      const response = await fetch('/api/charts/listening_time')
      const data = await response.json()

      if (data.labels && data.values) {
        this.createLineChart(
          'timeChart',
          data.labels,
          data.values,
          'Padrão de Escuta por Horário'
        )
      } else {
        this.showChartPlaceholder(
          'timeChart',
          'Sem dados de horário disponíveis'
        )
      }
    } catch (error) {
      console.error('Erro ao carregar gráfico de horários:', error)
      this.showChartError('timeChart', 'Erro ao carregar horários')
    }
  }

  async loadAudioFeaturesChart() {
    try {
      const response = await fetch('/api/charts/audio_features')
      const data = await response.json()

      if (data && Object.keys(data).length > 0) {
        this.createRadarChart(
          'audioFeaturesChart',
          data,
          'Características das Suas Músicas'
        )
      } else {
        this.showChartPlaceholder(
          'audioFeaturesChart',
          'Sem dados de características disponíveis'
        )
      }
    } catch (error) {
      console.error('Erro ao carregar características de áudio:', error)
      // Não mostrar erro para este gráfico se não existir o canvas
      const canvas = document.getElementById('audioFeaturesChart')
      if (!canvas) return
      this.showChartError(
        'audioFeaturesChart',
        'Erro ao carregar características'
      )
    }
  }

  createPieChart(canvasId, labels, data, title) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const ctx = canvas.getContext('2d')

    // Destruir gráfico existente se houver
    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy()
    }

    this.charts[canvasId] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels.map((label) => this.capitalizeFirst(label)),
        datasets: [
          {
            data: data,
            backgroundColor: [
              '#1DB954',
              '#1ed760',
              '#1df85f',
              '#ff6b6b',
              '#4ecdc4',
              '#45b7d1',
              '#f9ca24',
              '#f0932b',
              '#eb4d4b',
              '#6c5ce7',
              '#a29bfe',
              '#fd79a8',
              '#fdcb6e',
              '#e17055',
              '#74b9ff',
            ],
            borderWidth: 2,
            borderColor: '#fff',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
          },
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              usePointStyle: true,
              font: {
                size: 12,
              },
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.label || ''
                const value = context.parsed
                const total = context.dataset.data.reduce((a, b) => a + b, 0)
                const percentage = ((value / total) * 100).toFixed(1)
                return `${label}: ${value} (${percentage}%)`
              },
            },
          },
        },
      },
    })
  }

  createLineChart(canvasId, labels, data, title) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const ctx = canvas.getContext('2d')

    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy()
    }

    this.charts[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Músicas Tocadas',
            data: data,
            borderColor: '#1DB954',
            backgroundColor: 'rgba(29, 185, 84, 0.1)',
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#1DB954',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
          },
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)',
            },
            ticks: {
              font: {
                size: 11,
              },
            },
          },
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)',
            },
            ticks: {
              font: {
                size: 11,
              },
            },
          },
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
      },
    })
  }

  createRadarChart(canvasId, data, title) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const ctx = canvas.getContext('2d')

    if (this.charts[canvasId]) {
      this.charts[canvasId].destroy()
    }

    // Verificar se data tem a estrutura correta
    let labels, values
    if (data.labels && data.values) {
      // Formato correto: {labels: [...], values: [...]}
      labels = data.labels
      values = data.values
    } else {
      // Formato alternativo: objeto com características
      const features = Object.keys(data)
      values = features.map((feature) => data[feature])
      labels = features.map((feature) => this.formatFeatureName(feature))
    }

    this.charts[canvasId] = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Suas Músicas',
            data: values,
            borderColor: '#1DB954',
            backgroundColor: 'rgba(29, 185, 84, 0.2)',
            pointBackgroundColor: '#1DB954',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7,
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: false,
          },
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = (context.parsed.r * 100).toFixed(1);
                return `${label}: ${value}%`;
              }
            }
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 1,
            min: 0,
            ticks: {
              stepSize: 0.2,
              callback: function(value) {
                return (value * 100).toFixed(0) + '%';
              },
              font: {
                size: 10
              },
              display: false  // Ocultar números no mobile
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.1)',
            },
            pointLabels: {
              font: {
                size: window.innerWidth < 768 ? 10 : 12,
                weight: 'bold'
              },
              color: '#333'
            },
          },
        },
      },
    })
  }

  showChartPlaceholder(canvasId, message) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const container = canvas.parentElement
    container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-chart-bar fa-3x"></i>
                <p class="mb-0">${message}</p>
            </div>
        `
  }

  showChartError(canvasId, message) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const container = canvas.parentElement
    container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle fa-3x text-warning"></i>
                <p class="mb-0">${message}</p>
                <button class="btn btn-sm btn-outline-secondary mt-2" onclick="dashboardManager.loadAllCharts()">
                    <i class="fas fa-refresh me-1"></i>Tentar Novamente
                </button>
            </div>
        `
  }

  async refreshAllData() {
    console.log('🔄 Atualizando dados...')

    // Mostrar loading
    this.showLoadingState()

    try {
      // Recarregar página para buscar dados atualizados
      window.location.reload()
    } catch (error) {
      console.error('Erro ao atualizar dados:', error)
      this.showError('Erro ao atualizar dados')
    }
  }

  showLoadingState() {
    const loadingElements = document.querySelectorAll('.chart-card .card-body')
    loadingElements.forEach((element) => {
      element.innerHTML = `
                <div class="error-state">
                    <div class="loading"></div>
                    <p class="mt-2 mb-0">Carregando...</p>
                </div>
            `
    })
  }

  showError(message) {
    // Criar toast de erro
    const toast = document.createElement('div')
    toast.className = 'toast align-items-center text-white bg-danger border-0'
    toast.setAttribute('role', 'alert')
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-triangle me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `

    // Adicionar ao container de toasts (criar se não existir)
    let toastContainer = document.querySelector('.toast-container')
    if (!toastContainer) {
      toastContainer = document.createElement('div')
      toastContainer.className =
        'toast-container position-fixed top-0 end-0 p-3'
      document.body.appendChild(toastContainer)
    }

    toastContainer.appendChild(toast)

    // Mostrar toast
    const bsToast = new bootstrap.Toast(toast)
    bsToast.show()
  }

  capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1)
  }

  formatFeatureName(feature) {
    const nameMap = {
      danceability: 'Dançabilidade',
      energy: 'Energia',
      speechiness: 'Fala',
      acousticness: 'Acústico',
      instrumentalness: 'Instrumental',
      liveness: 'Ao Vivo',
      valence: 'Positividade',
    }
    return nameMap[feature] || this.capitalizeFirst(feature)
  }
}

// Inicializar quando a página carregar
let dashboardManager
document.addEventListener('DOMContentLoaded', function () {
  dashboardManager = new DashboardManager()
})

// Funções globais para compatibilidade
function loadGenresChart() {
  if (dashboardManager) {
    dashboardManager.loadGenresChart()
  }
}

function loadTimeChart() {
  if (dashboardManager) {
    dashboardManager.loadTimeChart()
  }
}

function createPieChart(canvasId, labels, data, title) {
  if (dashboardManager) {
    dashboardManager.createPieChart(canvasId, labels, data, title)
  }
}

function createLineChart(canvasId, labels, data, title) {
  if (dashboardManager) {
    dashboardManager.createLineChart(canvasId, labels, data, title)
  }
}
