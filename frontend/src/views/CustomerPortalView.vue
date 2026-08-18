<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="page-title">Customer Portal</h1>
    
    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div class="lg:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-2">Select Customer</label>
          <select
            v-model="selectedCustomer"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            @change="loadPortal"
          >
            <option value="">-- Choose Customer --</option>
            <option v-for="c in store.customerOptions" :key="c.value" :value="c.value">
              {{ c.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">From Date</label>
          <input
            type="date"
            v-model="fromDate"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            @change="loadPortal"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">To Date</label>
          <input
            type="date"
            v-model="toDate"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            @change="loadPortal"
          />
        </div>
        <div class="flex items-end">
          <button
            class="w-full rounded-lg bg-indigo-600 text-white px-4 py-2 text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            @click="loadPortal"
            :disabled="!selectedCustomer"
          >
            View Portal
          </button>
        </div>
      </div>
    </div>

    <div v-if="portal && selectedCustomer" class="space-y-6">
      <div class="bg-white rounded-xl shadow p-6 border border-gray-200">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <h2 class="text-2xl font-semibold text-gray-900">{{ portal.customer?.name || '-' }}</h2>
            <p class="text-sm text-gray-500 mt-2">
              {{ portal.customer?.customer_id || '-' }} · {{ portal.customer?.village || '-' }} · {{ portal.customer?.phone || '-' }}
            </p>
          </div>
          <div class="rounded-2xl bg-indigo-50 px-5 py-4 text-right">
            <p class="text-xs uppercase tracking-wide text-indigo-500">Balance Due</p>
            <p class="mt-1 text-3xl font-bold text-indigo-900">₹{{ formatNumber(portal?.balance_due) }}</p>
            <button
              @click="navigateToPayments"
              class="mt-4 inline-flex items-center justify-center rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
            >
              Go to Payment
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl shadow p-5 border border-gray-200">
          <p class="text-sm font-medium text-gray-500">Total Entries</p>
          <p class="mt-3 text-2xl font-semibold text-gray-900">{{ portal?.total_entries || 0 }}</p>
        </div>
        <div class="bg-white rounded-xl shadow p-5 border border-gray-200">
          <p class="text-sm font-medium text-gray-500">Total Milk</p>
          <p class="mt-3 text-2xl font-semibold text-gray-900">{{ formatNumber(portal?.total_milk) }} L</p>
        </div>
        <div class="bg-white rounded-xl shadow p-5 border border-gray-200">
          <p class="text-sm font-medium text-gray-500">Total Amount</p>
          <p class="mt-3 text-2xl font-semibold text-gray-900">₹{{ formatNumber(portal?.total_amount) }}</p>
        </div>
        <div class="bg-white rounded-xl shadow p-5 border border-gray-200">
          <p class="text-sm font-medium text-gray-500">Period Start</p>
          <p class="mt-3 text-2xl font-semibold text-gray-900">{{ portal?.date_range?.from ? formatDate(portal.date_range.from) : '-' }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <div class="bg-white rounded-xl shadow overflow-hidden border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">Collection History</h3>
          </div>
          <div>
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50 sticky top-0 z-10">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Session</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Qty (L)</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="(row, index) in historyRows"
                  :key="row.date"
                  :tabindex="0"
                  :class="[
                    'transition-colors outline-none cursor-pointer',
                    selectedHistoryIndex === index ? 'bg-red-200 ring-1 ring-red-200' : 'hover:bg-gray-50'
                  ]"
                  @click="selectHistoryRow(index)"
                  @keydown="onHistoryRowKeydown($event, index)"
                  :ref="el => setHistoryRowRef(el, index)"
                >
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(row.date) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center gap-2">
                      <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium', row.am > 0 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500']">
                        AM: {{ formatNumber(row.am) }}
                      </span>
                      <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium', row.pm > 0 ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-500']">
                        PM: {{ formatNumber(row.pm) }}
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                    {{ formatNumber(row.total) }}
                  </td>
                </tr>
                <tr v-if="!(historyRows.length > 0)">
                  <td colspan="3" class="px-6 py-8 text-center text-gray-500">No records found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow overflow-hidden border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">Payment Records</h3>
          </div>
          <div>
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50 sticky top-0 z-10">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">From</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">To</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Notes</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="p in portal?.payments || []" :key="p.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(p.from_date) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(p.end_date) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">₹{{ p.recorded_amount }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span :class="['inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium', getStatusClass(p.status)]">
                      {{ p.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ p.notes || '-' }}</td>
                </tr>
                <tr v-if="!(portal?.payments?.length > 0)">
                  <td colspan="5" class="px-6 py-8 text-center text-gray-500">No payment records</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!selectedCustomer" class="bg-white rounded-xl shadow p-10 text-center border border-gray-200">
      <div class="text-5xl mb-4">👤</div>
      <h3 class="text-lg font-semibold text-gray-900">Select a customer to view their portal</h3>
      <p class="mt-2 text-gray-500">View collection history, payments, and balance details.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMilkStore } from '../stores/milkStore'

const store = useMilkStore()
const route = useRoute()
const router = useRouter()

const selectedCustomer = ref(route.params.id || '')
const fromDate = ref('')
const toDate = ref('')
const selectedHistoryIndex = ref(0)
const historyRowRefs = ref([])

const portal = computed(() => store.customerPortal)

const historyRows = computed(() => {
  const grouped = new Map()

  for (const entry of portal.value?.entries || []) {
    const key = entry.date
    if (!grouped.has(key)) {
      grouped.set(key, {
        date: key,
        am: 0,
        pm: 0,
        total: 0
      })
    }

    const row = grouped.get(key)
    const quantity = Number(entry.quantity || 0)

    if (entry.session === 'AM') row.am = quantity
    if (entry.session === 'PM') row.pm = quantity
    row.total = Number((row.am + row.pm).toFixed(2))
  }

  return [...grouped.values()].sort((a, b) => new Date(b.date) - new Date(a.date))
})

const setHistoryRowRef = (el, index) => {
  if (el) {
    historyRowRefs.value[index] = el
  }
}

const selectHistoryRow = (index) => {
  selectedHistoryIndex.value = index
  nextTick(() => {
    historyRowRefs.value[index]?.focus()
  })
}

const onHistoryRowKeydown = (event, index) => {
  if (event.key === 'Tab' || event.key === 'ArrowDown') {
    event.preventDefault()
    const nextIndex = Math.min(index + 1, historyRows.value.length - 1)
    selectHistoryRow(nextIndex)
    return
  }

  if (event.key === 'ArrowUp') {
    event.preventDefault()
    const prevIndex = Math.max(index - 1, 0)
    selectHistoryRow(prevIndex)
  }
}

const formatNumber = (val) => {
  if (val === null || val === undefined || val === '') return '0.00'
  return Number(val).toFixed(2)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

const getStatusClass = (status) => {
  const map = {
    'Paid': 'badge-success',
    'Part Paid': 'badge-warning',
    'Pending': 'badge-danger',
    'Under Review': 'badge-warning'
  }
  return map[status] || 'badge-secondary'
}

const loadPortal = () => {
  if (!selectedCustomer.value) return
  const params = {}
  if (fromDate.value) params.from_date = fromDate.value
  if (toDate.value) params.to_date = toDate.value
  store.fetchCustomerPortal(selectedCustomer.value, params)
}

const navigateToPayments = () => {
  if (!selectedCustomer.value) return
  const customerId = selectedCustomer.value || portal?.customer?.customer_id || ''
  const paymentDateFrom = fromDate.value || portal?.date_range?.from || ''
  const paymentDateTo = toDate.value || portal?.date_range?.to || ''
  const amount = portal?.value?.balance_due ? Number(portal?.value?.balance_due) : 0

  store.setPaymentContext({
    customer_id: customerId,
    from_date: paymentDateFrom,
    end_date: paymentDateTo,
    amount
  })

  router.push({ name: 'Payments' })
}

onMounted(() => {
  store.fetchCustomers()
  if (selectedCustomer.value) {
    loadPortal()
  }
})
</script>

<style scoped>
.page-title {
  margin-bottom: 24px;
  font-size: 1.75rem;
  color: #1a237e;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-label {
  font-size: 0.85rem;
  color: #666;
  margin-top: 4px;
}
</style>