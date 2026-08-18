<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Payment Records</h1>

    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Record Payment</h3>
          <p class="text-sm text-gray-500">Use the form below to add a payment. Values from the portal are pre-filled.</p>
        </div>
        <div class="rounded-2xl bg-indigo-50 px-4 py-3 text-sm text-indigo-900">
          <p class="font-semibold">Balance Due</p>
          <p class="mt-1 text-xl font-bold">₹{{ balanceDue.toFixed(2) }}</p>
        </div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Customer</label>
          <select
            v-model="form.customer_id"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">Select Customer</option>
            <option v-for="c in store.customerOptions" :key="c.value" :value="c.value">
              {{ c.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">From Date</label>
          <input
            type="date"
            v-model="form.from_date"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">To Date</label>
          <input
            type="date"
            v-model="form.end_date"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Amount (₹)</label>
          <input
            type="number"
            v-model.number="form.recorded_amount"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            v-model="form.status"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="Paid">Paid</option>
            <option value="Part Paid">Part Paid</option>
            <option value="Pending">Pending</option>
            <option value="Under Review">Under Review</option>
          </select>
        </div>
        <div class="sm:col-span-2 lg:col-span-3">
          <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
          <input
            v-model="form.notes"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Optional notes"
          />
        </div>
      </div>
      <div class="mt-4 flex items-center justify-between">
        <button
          @click="resetForm"
          class="px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Clear
        </button>
        <button
          @click="savePayment"
          :disabled="!isValid"
          class="px-4 py-2 rounded-lg bg-green-600 text-white text-sm font-medium hover:bg-green-700 disabled:opacity-50"
        >
          Save Payment
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">All Payment Records</h3>
        <div class="mt-2">
          <button
            @click="exportPayments"
            class="rounded-lg bg-indigo-600 text-white px-3 py-2 text-sm font-medium hover:bg-indigo-700"
          >
            Export to Google Sheets
          </button>
        </div>
      </div>
      <div :class="store.payments.length > 20 ? 'max-h-96 overflow-y-auto' : ''">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">From</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">To</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Amount</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Notes</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"></th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="p in store.payments" :key="p.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ p.customer?.name || p.customer_id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(p.from_date) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(p.end_date) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">
              ₹{{ Number(p.recorded_amount).toFixed(2) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  statusBadgeClass(p.status)
                ]"
              >
                {{ p.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ p.notes || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click="removePayment(p.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="store.payments.length === 0">
            <td colspan="7" class="px-6 py-12 text-center text-gray-500">No payment records found</td>
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

const form = ref({
  customer_id: '',
  from_date: new Date().toISOString().split('T')[0],
  end_date: new Date().toISOString().split('T')[0],
  recorded_amount: 0,
  status: 'Paid',
  notes: ''
})
const balanceDue = ref(0)

const isValid = computed(() => {
  return form.value.customer_id && form.value.recorded_amount > 0
})

const statusBadgeClass = (status) => {
  const map = {
    'Paid': 'bg-green-100 text-green-800',
    'Part Paid': 'bg-amber-100 text-amber-800',
    'Pending': 'bg-red-100 text-red-800',
    'Under Review': 'bg-blue-100 text-blue-800'
  }
  return map[status] || 'bg-gray-100 text-gray-800'
}

const savePayment = async () => {
  try {
    await store.createPayment(form.value)
    toast.success('Payment recorded successfully')
    resetForm()
    store.fetchPayments()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to save payment')
  }
}

const resetForm = () => {
  form.value = {
    customer_id: '',
    from_date: new Date().toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0],
    recorded_amount: 0,
    status: 'Paid',
    notes: ''
  }
}

const removePayment = async (id) => {
  if (!confirm('Delete this payment record?')) return
  try {
    await store.deletePayment(id)
    toast.success('Payment deleted')
    store.fetchPayments()
  } catch (err) {
    toast.error('Failed to delete payment')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

const loadPaymentContext = () => {
  const context = store.paymentContext || {}
  if (context.customer_id) form.value.customer_id = context.customer_id
  if (context.from_date) form.value.from_date = context.from_date
  if (context.end_date) form.value.end_date = context.end_date
  if (context.amount != null) {
    balanceDue.value = Number(context.amount)
    form.value.recorded_amount = Number(context.amount)
  }
}

const exportPayments = async () => {
  try {
    const payload = store.payments.map(p => ({
      customer_id: p.customer_id || p.customer?.customer_id || p.customer?.id,
      from_date: p.from_date,
      end_date: p.end_date,
      recorded_amount: p.recorded_amount,
      status: p.status,
      notes: p.notes
    }))
    await axios.post(`${API_URL}/export/payments`, payload)
    toast.success('Exported payments to Google Sheet')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Failed to export payments')
  }
}

onMounted(() => {
  store.fetchCustomers()
  store.fetchPayments()
  loadPaymentContext()
})
</script>