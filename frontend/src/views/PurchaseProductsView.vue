<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Purchase Products</h1>
      <p class="mt-1 text-sm text-gray-500">Choose a customer, add products, and track payment status.</p>
    </div>

    <section class="bg-white rounded-xl shadow p-6 mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-1" for="purchase-customer">Customer</label>
      <select
        id="purchase-customer"
        v-model="selectedCustomerId"
        class="w-full max-w-xl rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="">Select Customer</option>
        <option v-for="customer in store.customers" :key="customer.id" :value="customer.customer_id">
          {{ customer.customer_id }} - {{ customer.name }}
        </option>
      </select>
    </section>

    <section v-if="selectedCustomerId" class="bg-white rounded-xl shadow overflow-hidden mb-6">
      <div class="p-4 border-b border-gray-200 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Available Products</h2>
          <p class="mt-1 text-sm text-gray-500">Add a product, then adjust its quantity in the purchase grid.</p>
        </div>
        <div class="w-full sm:w-72">
          <label class="block text-xs font-medium uppercase tracking-wide text-gray-500 mb-1" for="product-search">Search Products</label>
          <input id="product-search" v-model.trim="productSearch" type="search" placeholder="Search by name or description" class="w-full rounded-lg border-gray-300 border px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
        </div>
      </div>
      <div class="p-4 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <article v-for="product in filteredProducts" :key="product.id" class="rounded-lg border border-gray-200 p-4 flex flex-col min-h-56 hover:border-indigo-300">
          <div class="flex items-start justify-between gap-3">
            <h3 class="font-semibold text-gray-900 break-words">{{ product.product_name }}</h3>
            <span
              :class="Number(product.quantity) > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
              class="shrink-0 rounded-full px-2 py-1 text-xs font-medium"
            >
              {{ Number(product.quantity) > 0 ? 'Available' : 'Out of stock' }}
            </span>
          </div>
          <p class="mt-2 text-sm text-gray-500 min-h-10">{{ product.description || 'No description added.' }}</p>
          <dl class="mt-4 grid grid-cols-3 gap-2 text-sm">
            <div><dt class="text-xs text-gray-500">Stock</dt><dd class="mt-1 font-semibold text-gray-900">{{ formatNumber(product.quantity) }}</dd></div>
            <div><dt class="text-xs text-gray-500">Size</dt><dd class="mt-1 font-semibold text-gray-900">{{ product.size || '-' }}</dd></div>
            <div><dt class="text-xs text-gray-500">Price</dt><dd class="mt-1 font-semibold text-gray-900">₹{{ formatNumber(product.price) }}</dd></div>
          </dl>
          <button type="button" @click="addProduct(product)" class="mt-auto w-full rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700">
            Add Product
          </button>
        </article>
        <p v-if="filteredProducts.length === 0" class="sm:col-span-2 xl:col-span-4 px-6 py-10 text-center text-gray-500">
          No matching active products with available quantity.
        </p>
      </div>
    </section>

    <section v-if="selectedCustomerId" class="bg-white rounded-xl shadow overflow-hidden mb-6">
      <div class="p-4 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">Purchase Grid</h2>
          <p class="mt-1 text-sm text-gray-500">Review quantities and payment status before saving.</p>
        </div>
        <div class="text-right">
          <p class="text-xs uppercase tracking-wide text-gray-500">Amount Payable</p>
          <p class="text-2xl font-bold text-indigo-700">₹{{ formatNumber(draftTotal) }}</p>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-heading">Product</th>
              <th class="table-heading">Description</th>
              <th style="display: none;" class="table-heading">Size</th>
              <th class="table-heading text-right">Price</th>
              <th class="table-heading text-right">Quantity</th>
              <th class="table-heading text-right">Amount Payable</th>
              <th class="table-heading text-center">Paid</th>
              <th class="table-heading"></th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in draftPurchases" :key="item.product_id">
              <td class="table-cell font-medium text-gray-900">{{ item.product.product_name }}</td>
              <td class="table-cell text-gray-500">{{ item.product.description || '-' }}</td>
              <td  style="display: none;" class="table-cell text-gray-500">{{ item.product.size || '-' }}</td>
              <td class="table-cell text-right">₹{{ formatNumber(item.product.price) }}</td>
              <td class="table-cell text-right">
                <input v-model.number="item.quantity" type="number" min="0.01" :max="item.maxQuantity" step="0.01" class="w-24 rounded-lg border-gray-300 border px-2 py-1 text-sm text-right focus:ring-indigo-500 focus:border-indigo-500" />
              </td>
              <td class="table-cell text-right font-semibold">₹{{ formatNumber(item.quantity * item.product.price) }}</td>
              <td class="table-cell text-center"><input v-model="item.paid" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" /></td>
              <td class="table-cell text-right"><button type="button" @click="removeDraft(item.product_id)" class="text-sm text-red-600 hover:text-red-900">Remove</button></td>
            </tr>
            <tr v-if="draftPurchases.length === 0">
              <td colspan="8" class="px-6 py-10 text-center text-gray-500">Add products above to build this purchase.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="p-4 border-t border-gray-200 flex justify-end">
        <button type="button" @click="savePurchases" :disabled="draftPurchases.length === 0 || saving" class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50">
          {{ saving ? 'Saving...' : 'Save Purchase' }}
        </button>
      </div>
    </section>

    <section v-if="selectedCustomerId" class="bg-white rounded-xl shadow overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Purchased Products</h2>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="table-heading">Product</th>
              <th class="table-heading">Description</th>
              <th class="table-heading">Size</th>
              <th class="table-heading text-right">Price</th>
              <th class="table-heading text-right">Quantity</th>
              <th class="table-heading text-right">Amount</th>
              <th class="table-heading text-center">Paid</th>
              <th class="table-heading text-right"></th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="purchase in store.purchases" :key="purchase.id">
              <td class="table-cell font-medium text-gray-900">{{ purchase.product.product_name }}</td>
              <td class="table-cell text-gray-500">{{ purchase.product.description || '-' }}</td>
              <td class="table-cell text-gray-500">{{ purchase.product.size || '-' }}</td>
              <td class="table-cell text-right">₹{{ formatNumber(purchase.unit_price) }}</td>
              <td class="table-cell text-right">{{ formatNumber(purchase.quantity) }}</td>
              <td class="table-cell text-right font-semibold">₹{{ formatNumber(purchase.amount) }}</td>
              <td class="table-cell text-center">
                <input :checked="purchase.paid" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" @change="togglePaid(purchase)" />
              </td>
              <td class="table-cell text-right"><button type="button" @click="deletePurchase(purchase)" class="text-sm font-medium text-red-600 hover:text-red-900">Delete</button></td>
            </tr>
            <tr v-if="store.purchases.length === 0">
              <td colspan="8" class="px-6 py-10 text-center text-gray-500">No purchased products for this customer.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useToast } from 'vue-toastification'
import { useMilkStore } from '../stores/milkStore'

const store = useMilkStore()
const toast = useToast()
const selectedCustomerId = ref('')
const productSearch = ref('')
const draftPurchases = ref([])
const saving = ref(false)

const availableProducts = computed(() => store.products.filter(product => product.active))
const filteredProducts = computed(() => {
  const search = productSearch.value.toLowerCase()
  if (!search) return availableProducts.value
  return availableProducts.value.filter(product => [product.product_name, product.description, product.size]
    .filter(Boolean)
    .some(value => value.toLowerCase().includes(search)))
})
const draftTotal = computed(() => draftPurchases.value.reduce((total, item) => total + Number(item.quantity || 0) * Number(item.product.price || 0), 0))
const formatNumber = value => Number(value || 0).toFixed(2)

const loadCustomerPurchases = async customerId => {
  draftPurchases.value = []
  if (!customerId) {
    store.purchases = []
    return
  }
  try {
    await store.fetchPurchases(customerId)
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to load purchased products')
  }
}

const addProduct = product => {
  const quantity = 1
  const existing = draftPurchases.value.find(item => item.product_id === product.id)
  if (existing) {
    existing.quantity = Math.min(existing.maxQuantity, Number(existing.quantity) + quantity)
  } else {
    draftPurchases.value.push({
      product_id: product.id,
      product,
      quantity,
      maxQuantity: Number(product.quantity),
      paid: false
    })
  }
}

const removeDraft = productId => {
  draftPurchases.value = draftPurchases.value.filter(item => item.product_id !== productId)
}

const savePurchases = async () => {
  saving.value = true
  try {
    for (const item of draftPurchases.value) {
      await store.createPurchase({
        customer_id: selectedCustomerId.value,
        product_id: item.product_id,
        quantity: Number(item.quantity),
        paid: item.paid
      })
    }
    toast.success('Purchase saved')
    draftPurchases.value = []
    await store.fetchProducts()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to save purchase')
    await store.fetchPurchases(selectedCustomerId.value)
  } finally {
    saving.value = false
  }
}

const togglePaid = async purchase => {
  try {
    await store.updatePurchasePaid(purchase.id, !purchase.paid)
    toast.success('Payment status updated')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to update payment status')
  }
}

const deletePurchase = async purchase => {
    debugger
  const productName = purchase.product?.product_name || 'this product'
  if (!window.confirm(`Delete ${productName} purchase? Stock will be restored.`)) return
  try {
    await store.deletePurchase(purchase.id)
    await store.fetchProducts()
    toast.success('Purchase deleted')
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to delete purchase')
  }
}

watch(selectedCustomerId, loadCustomerPurchases)

onMounted(async () => {
  try {
    await Promise.all([store.fetchCustomers(), store.fetchProducts()])
  } catch (err) {
    toast.error('Unable to load customers or products')
  }
})
</script>

<style scoped>
.table-heading {
  @apply px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500;
}

.table-cell {
  @apply px-4 py-3 text-sm;
}
</style>
