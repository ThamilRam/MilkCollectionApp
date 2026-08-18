<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Daily Milk Collection Entry</h1>

    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">New Entry</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            type="date"
            v-model="newEntry.date"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Session</label>
          <select
            v-model="newEntry.session"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="AM">Morning (AM)</option>
            <option value="PM">Evening (PM)</option>
          </select>
        </div>
        <div class="lg:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Customer</label>
          <select
            v-model="newEntry.customer_id"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">Select Customer</option>
            <option v-for="c in store.customerOptions" :key="c.value" :value="c.value">
              {{ c.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Qty (L)</label>
          <input
            type="number"
            step="0.1"
            v-model.number="newEntry.quantity"
            @input="calculateAmount"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Rate (₹)</label>
          <input
            type="number"
            v-model.number="newEntry.rate"
            @input="calculateAmount"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
      <div class="mt-4 flex items-center justify-between">
        <div class="text-lg font-semibold text-gray-900">
          Amount: ₹{{ newEntry.amount.toFixed(2) }}
        </div>
        <div class="flex gap-3">
          <button
            @click="resetForm"
            class="px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Clear
          </button>
          <button
            @click="saveEntry"
            :disabled="!isValid"
            class="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            Save Entry
          </button>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div
        class="p-4 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <h3 class="text-lg font-semibold text-gray-900">Recent Entries</h3>
        <div class="flex gap-3">
          <select
            v-model="filterSession"
            @change="loadEntries"
            class="rounded-lg border-gray-300 border px-3 py-2 text-sm"
          >
            <option value="">All Sessions</option>
            <option value="AM">AM</option>
            <option value="PM">PM</option>
          </select>
          <input
            type="date"
            v-model="filterFromDate"
            @change="loadEntries"
            class="rounded-lg border-gray-300 border px-3 py-2 text-sm"
          />
          <input disabled style="display: none;"
            type="date"
            v-model="filterToDate"
            @change="loadEntries"
            class="rounded-lg border-gray-300 border px-3 py-2 text-sm"
          />
          <button
            @click="exportEntries"
            class="rounded-lg bg-indigo-600 text-white px-3 py-2 text-sm font-medium hover:bg-indigo-700"
          >
            Export to Google Sheets
          </button>
        </div>
      </div>
      <div :class="store.entries.length > 20 ? 'max-h-96 overflow-y-auto' : ''">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Session
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              Customer
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Qty</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Rate</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
              Amount
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"></th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="entry in store.entries" :key="entry.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ formatDate(entry.date) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  entry.session === 'AM' ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'
                ]"
              >
                {{ entry.session }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ entry.customer?.name || entry.customer_id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
              {{ entry.quantity }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
              {{ entry.rate }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
              ₹{{ entry.amount }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="removeEntry(entry.id)" class="text-red-600 hover:text-red-900">
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="store.entries.length === 0">
            <td colspan="7" class="px-6 py-12 text-center text-gray-500">No entries found</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMilkStore } from '../stores/milkStore'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://milkcollectionapi.onrender.com/api/v1'

const store = useMilkStore()
const toast = useToast()

const newEntry = ref({
  date: new Date().toISOString().split('T')[0],
  session: 'AM',
  customer_id: '',
  quantity: 0,
  rate: 35,
  amount: 0
})

const filterSession = ref('')
const filterFromDate = ref(new Date())
const filterToDate = ref(new Date())

const isValid = computed(() => {
  return (
    newEntry.value.date &&
    newEntry.value.session &&
    newEntry.value.customer_id &&
    newEntry.value.quantity > 0
  )
})

const calculateAmount = () => {
  newEntry.value.amount = Number((newEntry.value.quantity * newEntry.value.rate).toFixed(2))
}

const saveEntry = async () => {
  try {
    await store.createEntry(newEntry.value)
    toast.success('Entry saved successfully')
    resetForm()
    loadEntries()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to save entry')
  }
}

const resetForm = () => {
  newEntry.value = {
    date: new Date().toISOString().split('T')[0],
    session: 'AM',
    customer_id: '',
    quantity: 0,
    rate: 35,
    amount: 0
  }
}

const loadEntries = () => {
  const params = {}
  if (filterSession.value) params.session = filterSession.value
  if (filterFromDate.value) {
    params.from_date = filterFromDate.value
    params.to_date = filterFromDate.value
  }
  //if (filterToDate.value) params.to_date = filterToDate.value
  store.fetchEntries(params)
}

const exportEntries = async () => {
  try {
    const payload = store.entries.map(e => ({
      date: e.date,
      session: e.session,
      customer_id: e.customer_id || e.customer?.customer_id || e.customer?.id,
      quantity: e.quantity,
      rate: e.rate,
      amount: e.amount
    }))
    await axios.post(`${API_URL}/export/daily-entries`, payload)
    toast.success('Exported entries to Google Sheet')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to export entries')
  }
}

const removeEntry = async (id) => {
  if (!confirm('Delete this entry?')) return
  try {
    await store.deleteEntry(id)
    toast.success('Entry deleted')
    loadEntries()
  } catch (err) {
    toast.error('Failed to delete entry')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(() => {
  store.fetchCustomers()
  loadEntries()
})
</script>