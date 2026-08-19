<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Bulk Daily Entry</h1>

    <!-- Control Panel -->
    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            type="date"
            v-model="entryDate"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Session</label>
          <select
            v-model="entrySession"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="AM">Morning (AM)</option>
            <option value="PM">Evening (PM)</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Default Rate (₹/L)</label>
          <input
            type="number"
            v-model.number="defaultRate"
            @change="applyRateToAll"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />          
        </div>
      </div>
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-500">
          <span class="font-medium text-gray-900">{{ validRows.length }}</span> entries ready to save
        </div>
        <div class="flex gap-3">
          <button
            type="button"
            @click="openSettingsModal"
            class="px-4 py-2 rounded-lg bg-rose-500 text-white text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            Update default rate
          </button>
          <button
            @click="loadCustomers"
            class="px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Reset Grid
          </button>
          <button
            @click="saveAll"
            :disabled="saving || validRows.length === 0"
            class="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ saving ? 'Saving...' : 'Save All Entries' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Entry Grid -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div :class="rows.length > 20 ? 'max-h-96 overflow-y-auto' : ''">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Customer ID
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Milk No
            </th>
            <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Qty (L)
            </th>
                <th  class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rate (₹)
                </th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount (₹)
                </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr
            v-for="(row, idx) in rows"
            :key="row.customer_id"
            :class="[
              'transition-colors',
              row.quantity > 0 ? 'bg-indigo-50/50' : 'hover:bg-gray-50'
            ]"
          >
            <td class="px-4 py-3 whitespace-nowrap text-sm font-bold text-gray-900">
              {{ row.customer_id }}
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
              {{ row.name }}
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
              {{ row.milk_no || '-' }}
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-right">
              <input
                type="number"
                step="0.1"
                min="0"
                v-model.number="row.quantity"
                @input="updateRowAmount(idx)"
                @keydown="onQtyKey($event, idx)"
                :ref="el => qtyInputs[idx] = el"
                class="w-24 rounded-lg border-gray-300 border px-2 py-1 text-sm text-right focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.0"
              />
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-right">
              <input
                type="number"
                v-model.number="row.rate"
                @input="updateRowAmount(idx)"
                class="w-20 rounded-lg border-gray-300 border px-2 py-1 text-sm text-right focus:ring-indigo-500 focus:border-indigo-500"
              />
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
              {{ (row.amount || 0).toFixed(2) }}
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="colCount" class="px-6 py-12 text-center text-gray-500">
              No active customers found
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <transition name="fade">
    <div
      v-if="showSettingsModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
      <div class="w-full max-w-md rounded-2xl bg-white shadow-xl ring-1 ring-black/10 overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">Update Default Rate</h2>
          <button @click="closeSettingsModal" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="px-6 py-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Default Rate (₹/L)</label>
              <input
                type="number"
                v-model.number="settingsRate"
                class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <p class="text-sm text-gray-500">This value is loaded from the settings table and saved back when you click Save.</p>
          </div>
        </div>
        <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-slate-50">
          <button
            type="button"
            @click="closeSettingsModal"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="saveSettings"
            :disabled="settingsSaving"
            class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ settingsSaving ? 'Saving...' : 'Save Settings' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const API_URL = import.meta.env.VITE_API_URL || 'https://milkcollectionapi.onrender.com/api/v1'
const toast = useToast()

const entryDate = ref(new Date().toISOString().split('T')[0])
const entrySession = ref('AM')
const defaultRate = ref(35)
const settingsRate = ref(35)
const showSettingsModal = ref(false)
const settingsSaving = ref(false)
const rows = ref([])
const saving = ref(false)

const validRows = computed(() => rows.value.filter(r => r.quantity > 0))
const colCount = computed(() => 6)

// Refs to quantity input elements so we can programmatically move focus
const qtyInputs = ref([])

const onQtyKey = (e, idx) => {
  const key = e.key
  if (key === 'Enter' || key === 'ArrowDown') {
    e.preventDefault()
    const next = Math.min(rows.value.length - 1, idx + 1)
    const el = qtyInputs.value[next]
    if (el && typeof el.focus === 'function') {
      el.focus()
      if (typeof el.select === 'function') el.select()
    }
  } else if (key === 'ArrowUp') {
    e.preventDefault()
    const prev = Math.max(0, idx - 1)
    const el = qtyInputs.value[prev]
    if (el && typeof el.focus === 'function') {
      el.focus()
      if (typeof el.select === 'function') el.select()
    }
  }
}

const updateRowAmount = (idx) => {
  const row = rows.value[idx]
  row.amount = Number((row.quantity * row.rate).toFixed(2))
}

const applyRateToAll = () => {
  rows.value.forEach(row => {
    row.rate = defaultRate.value
    if (row.quantity > 0) {
      row.amount = Number((row.quantity * row.rate).toFixed(2))
    }
  })
}

const openSettingsModal = async () => {
  showSettingsModal.value = true
  try {
    const { data: settings } = await axios.get(`${API_URL}/settings`)
    const loadedRate = settings.default_rate ?? settings.default_rate?.toString() ?? defaultRate.value
    settingsRate.value = Number(loadedRate) || defaultRate.value
  } catch (err) {
    toast.error('Failed to load default rate from settings')
  }
}

const closeSettingsModal = () => {
  showSettingsModal.value = false
}

const saveSettings = async () => {
  settingsSaving.value = true
  try {
    const value = String(settingsRate.value)
    await axios.put(`${API_URL}/settings/default_rate`, null, { params: { value } })
    defaultRate.value = Number(value)
    toast.success('Default rate updated successfully')
    closeSettingsModal()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to save settings')
  } finally {
    settingsSaving.value = false
  }
}

const loadCustomers = async () => {
  try {
    const { data: customers } = await axios.get(`${API_URL}/customers`)
    const { data: settings } = await axios.get(`${API_URL}/settings`)
    if (settings.default_rate) {
      defaultRate.value = Number(settings.default_rate)
    }
    rows.value = customers
      .filter(c => c.status === 'Active' && c.isMilkcustomer !== false)
      .map(c => ({
        customer_id: c.customer_id,
        name: c.name,
        milk_no: c.milk_no,
        quantity: 0,
        rate: defaultRate.value,
        amount: 0
      }))
  } catch (err) {
    toast.error('Failed to load customers')
  }
}

const saveAll = async () => {
  if (validRows.value.length === 0) {
    toast.warning('No entries to save')
    return
  }
  saving.value = true
  try {
    const payload = validRows.value.map(r => ({
      date: entryDate.value,
      session: entrySession.value,
      customer_id: r.customer_id,
      quantity: r.quantity,
      rate: r.rate,
      amount: r.amount
    }))
    await axios.post(`${API_URL}/daily-entries/bulk`, payload)
    toast.success(`${payload.length} entries saved successfully`)
    // Reset quantities but keep the grid
    rows.value.forEach(row => {
      row.quantity = 0
      row.amount = 0
    })
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to save entries')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadCustomers()
})
</script>