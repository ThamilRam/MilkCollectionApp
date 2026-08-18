<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Milk Collection Dashboard</h1>

    <div v-if="loading" class="text-center py-12 text-gray-500">Loading dashboard...</div>

    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="bg-white rounded-xl shadow p-6 flex items-center gap-4"
        >
          <div
            :class="['w-14 h-14 rounded-xl flex items-center justify-center text-2xl', stat.bg, stat.text]"
          >
            {{ stat.icon }}
          </div>
          <div>
            <div class="text-2xl font-bold text-gray-900">{{ stat.value }}</div>
            <div class="text-sm text-gray-500">{{ stat.label }}</div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow mb-6 p-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Date-wise Collection Report</h3>
          <div class="flex gap-3">
            <input
              type="date"
              v-model="fromDate"
              class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
            <input
              type="date"
              v-model="toDate"
              class="rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
            <button
              @click="loadDateWise"
              class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              Filter
            </button>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow overflow-hidden mb-6">
        <div :class="dateWiseData.length > 20 ? 'max-h-96 overflow-y-auto' : ''">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Date
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                AM(C)
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                PM(C)
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                AM Milk (L)
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                PM Milk (L)
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Total Milk (L)
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Amount (₹)
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="row in dateWiseData" :key="row.date" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(row.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {{ row.am_count }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                {{ row.pm_count }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium"
              >
                {{ formatNumber(row.am_milk) }}
              </td>              
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium"
              >
                {{ formatNumber(row.pm_milk) }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium"
              >
                {{ formatNumber(parseFloat(row.am_milk) + parseFloat(row.pm_milk)) }}
              </td>
              <td              
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium"
              >
                {{ formatNumber(row.total_amount) }}
              </td>
            </tr>
            <tr v-if="dateWiseData.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">No records found</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="bg-indigo-900 rounded-xl shadow p-6 text-white flex items-center justify-between">
        <div>
          <div class="text-indigo-200 text-sm">Grand Total Milk</div>
          <div class="text-2xl font-bold">{{ formatNumber(dashboard?.total_milk) }} L</div>
        </div>
        <div class="text-right">
          <div class="text-indigo-200 text-sm">Grand Total Amount</div>
          <div class="text-2xl font-bold">₹{{ formatNumber(dashboard?.total_amount) }}</div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMilkStore } from '../stores/milkStore'

const store = useMilkStore()
const fromDate = ref('')
const toDate = ref('')

const dashboard = computed(() => store.dashboard)
const dateWiseData = computed(() => store.dateWiseData)
const loading = computed(() => store.loading)

const stats = computed(() => [
  {
    icon: '👥',
    label: 'Active Customers',
    value: dashboard.value?.active_customers || 0,
    bg: 'bg-blue-100',
    text: 'text-blue-600'
  },
  {
    icon: '🥛',
    label: 'Today Milk',
    value: `${formatNumber(dashboard.value?.today_milk)} L`,
    bg: 'bg-green-100',
    text: 'text-green-600'
  },
  {
    icon: '💰',
    label: 'Today Amount',
    value: `₹${formatNumber(dashboard.value?.today_amount)}`,
    bg: 'bg-amber-100',
    text: 'text-amber-600'
  },
  {
    icon: '📅',
    label: 'This Month',
    value: `${formatNumber(dashboard.value?.month_milk)} L`,
    bg: 'bg-purple-100',
    text: 'text-purple-600'
  }
])

const formatNumber = (val) => {
  if (!val) return '0.00'
  return Number(val).toFixed(2)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

const loadDateWise = () => {
  const params = {}
  if (fromDate.value) params.from_date = fromDate.value
  if (toDate.value) params.to_date = toDate.value
  store.fetchDateWise(params)
}

onMounted(() => {
  store.fetchDashboard()
  store.fetchDateWise()
})
</script>