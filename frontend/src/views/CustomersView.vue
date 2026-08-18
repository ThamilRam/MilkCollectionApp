<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Customer Master</h1>

    <div class="bg-white rounded-xl shadow p-6 mb-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">
        {{ editing ? 'Edit Customer' : 'Add New Customer' }}
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Customer ID *</label>
          <input
            v-model="form.customer_id"
            :disabled="editing"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-100"
            placeholder="e.g. C003"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Name *</label>
          <input
            v-model="form.name"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Full Name"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Milk No</label>
          <input
            v-model="form.milk_no"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="M001"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
          <input
            v-model="form.phone"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Phone"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Village</label>
          <input
            v-model="form.village"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Village"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Opening Balance</label>
          <input
            type="number"
            v-model.number="form.opening_balance"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            v-model="form.status"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
          <input
            type="date"
            v-model="form.start_date"
            class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
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
          @click="saveCustomer"
          :disabled="!form.customer_id || !form.name"
          class="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
        >
          {{ editing ? 'Update' : 'Save' }} Customer
        </button>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Customer List</h3>
      </div>
      <div :class="store.customers.length > 20 ? 'max-h-96 overflow-y-auto' : ''">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Milk No</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Village</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Balance</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"></th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="c in store.customers" :key="c.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
              {{ c.customer_id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ c.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ c.milk_no || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ c.phone || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ c.village || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
              ₹{{ Number(c.opening_balance).toFixed(2) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  c.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                ]"
              >
                {{ c.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                @click="editCustomer(c)"
                class="text-indigo-600 hover:text-indigo-900 mr-3"
              >
                Edit
              </button>
              <router-link
                :to="`/portal/${c.customer_id}`"
                class="text-gray-600 hover:text-gray-900"
              >
                Portal
              </router-link>
            </td>
          </tr>
          <tr v-if="store.customers.length === 0">
            <td colspan="8" class="px-6 py-12 text-center text-gray-500">No customers found</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMilkStore } from '../stores/milkStore'
import { useToast } from 'vue-toastification'

const store = useMilkStore()
const toast = useToast()
const editing = ref(false)

const defaultForm = {
  customer_id: '',
  name: '',
  milk_no: '',
  phone: '',
  village: '',
  opening_balance: 0,
  status: 'Active',
  start_date: new Date().toISOString().split('T')[0]
}

const form = ref({ ...defaultForm })

const saveCustomer = async () => {
  try {
    if (editing.value) {
      await store.updateCustomer(form.value.customer_id, form.value)
      toast.success('Customer updated')
    } else {
      await store.createCustomer(form.value)
      toast.success('Customer created')
    }
    resetForm()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Operation failed')
  }
}

const editCustomer = (customer) => {
  form.value = {
    ...customer,
    start_date: customer.start_date || new Date().toISOString().split('T')[0]
  }
  editing.value = true
}

const resetForm = () => {
  form.value = { ...defaultForm }
  editing.value = false
}

onMounted(() => {
  store.fetchCustomers()
})
</script>