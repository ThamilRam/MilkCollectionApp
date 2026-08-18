<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Monthly Customer Reports</h1>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Customer Milk Trend</h2>
            <p class="text-sm text-gray-500">Month-wise milk quantity for selected customer</p>
          </div>
          <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <select v-model="selectedCustomer" @change="loadCustomerMonthly" class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto">
              <option disabled value="">Select customer</option>
              <option v-for="customer in customers" :key="customer.customer_id" :value="customer.customer_id">
                {{ customer.customer_id }} - {{ customer.name }}
              </option>
            </select>
            <select v-model.number="selectedYear" @change="loadCustomerMonthly" class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto">
              <option v-for="year in yearOptions" :key="year" :value="year">{{ year }}</option>
            </select>
          </div>
        </div>

        <div v-if="customerMonthlyData.length === 0" class="text-center py-16 text-gray-500">
          Select a customer to view the monthly line chart.
        </div>
        <div v-else class="h-[320px]">
          <canvas ref="lineCanvas" class="w-full h-full"></canvas>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Top 3 Customers</h2>
            <p class="text-sm text-gray-500">Top customers by milk quantity in selected month</p>
          </div>
          <div class="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <select v-model.number="selectedMonth" @change="loadTopCustomers" class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto">
              <option v-for="option in monthOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
            <select v-model.number="selectedYearMonth" @change="loadTopCustomers" class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-auto">
              <option v-for="year in yearOptions" :key="year" :value="year">{{ year }}</option>
            </select>
          </div>
        </div>

        <div v-if="topCustomers.length === 0" class="text-center py-16 text-gray-500">
          No top customer data available for the selected month.
        </div>
        <div v-else class="h-[320px]">
          <canvas ref="barCanvas" class="w-full h-full"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import { useMilkStore } from '../stores/milkStore'

const store = useMilkStore()
const lineCanvas = ref(null)
const barCanvas = ref(null)
let lineChart = null
let barChart = null

const selectedCustomer = ref('')
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth())
const selectedYearMonth = ref(new Date().getFullYear())

const monthOptions = [
  { value: 1, label: 'January' },
  { value: 2, label: 'February' },
  { value: 3, label: 'March' },
  { value: 4, label: 'April' },
  { value: 5, label: 'May' },
  { value: 6, label: 'June' },
  { value: 7, label: 'July' },
  { value: 8, label: 'August' },
  { value: 9, label: 'September' },
  { value: 10, label: 'October' },
  { value: 11, label: 'November' },
  { value: 12, label: 'December' }
]

const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  return [currentYear - 1, currentYear]
})

const customers = computed(() => store.customers)
const customerMonthlyData = computed(() => store.customerMonthlyData)
const topCustomers = computed(() => store.topCustomers)

const formatMonth = (month) => month.toString().padStart(2, '0')

const createLineChart = () => {
  if (!lineCanvas.value) return
  const ctx = lineCanvas.value.getContext('2d')
  if (lineChart) lineChart.destroy()
  const labels = Array.from({ length: 12 }, (_, i) => monthOptions[i].label)
  const data = Array(12).fill(0)
  customerMonthlyData.value.forEach((item) => {
    data[item.month - 1] = Number(item.total_milk)
  })
  lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Milk (L)',
        data,
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79,70,229,0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: 'Litres' }
        }
      }
    }
  })
}

const createBarChart = () => {
  if (!barCanvas.value) return
  const ctx = barCanvas.value.getContext('2d')
  if (barChart) barChart.destroy()
  const labels = topCustomers.value.map(item => item.customer_name)
  const data = topCustomers.value.map(item => Number(item.total_milk))
  barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Milk (L)',
        data,
        backgroundColor: ['#6366f1', '#34d399', '#f59e0b']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: 'Litres' }
        }
      }
    }
  })
}

const loadCustomerMonthly = async () => {
  if (!selectedCustomer.value) return
  await store.fetchCustomerMonthly(selectedCustomer.value, selectedYear.value)
}

const loadTopCustomers = async () => {
  await store.fetchTopCustomers(selectedMonth.value, selectedYearMonth.value)
}

watch(customerMonthlyData, () => {
  if (customerMonthlyData.value.length) createLineChart()
})

watch(topCustomers, () => {
  if (topCustomers.value.length) createBarChart()
})

onMounted(async () => {
  await store.fetchCustomers()
  const today = new Date()
  selectedMonth.value = today.getMonth() === 0 ? 12 : today.getMonth()
  selectedYearMonth.value = today.getMonth() === 0 ? today.getFullYear() - 1 : today.getFullYear()
  await loadTopCustomers()
})
</script>
