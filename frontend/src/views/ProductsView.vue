<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Products</h1>
        <p class="mt-1 text-sm text-gray-500">Manage your product catalogue and stock.</p>
      </div>
      <span class="text-sm text-gray-500">{{ store.products.length }} product{{ store.products.length === 1 ? '' : 's' }}</span>
    </div>

    <form class="bg-white rounded-xl shadow p-6 mb-6" @submit.prevent="saveProduct">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">
        {{ editing ? 'Edit Product' : 'Add New Product' }}
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="product-name">Product Name *</label>
          <input id="product-name" v-model.trim="form.product_name" required maxlength="150" class="form-input" placeholder="e.g. Fresh Milk" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="product-description">Description</label>
          <input id="product-description" v-model.trim="form.description" class="form-input" placeholder="Short description" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="product-size">Size</label>
          <input id="product-size" v-model.trim="form.size" maxlength="50" class="form-input" placeholder="e.g. 500 ml" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="product-quantity">Quantity</label>
          <input id="product-quantity" v-model.number="form.quantity" type="number" min="0" step="0.01" class="form-input" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1" for="product-price">Price</label>
          <input id="product-price" v-model.number="form.price" type="number" min="0" step="0.01" class="form-input" />
        </div>
        <label class="flex items-center gap-3 self-end min-h-10 text-sm font-medium text-gray-700">
          <input v-model="form.active" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
          Active product
        </label>
      </div>
      <div class="mt-5 flex items-center justify-end gap-3">
        <button v-if="editing" type="button" @click="resetForm" class="button-secondary">Cancel</button>
        <button type="submit" :disabled="!form.product_name || saving" class="button-primary">
          {{ saving ? 'Saving...' : editing ? 'Update Product' : 'Add Product' }}
        </button>
      </div>
    </form>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <article v-for="product in store.products" :key="product.id" class="bg-white rounded-xl shadow border border-gray-100 p-5 flex flex-col">
        <div class="flex items-start justify-between gap-3">
          <h2 class="text-lg font-semibold text-gray-900 break-words">{{ product.product_name }}</h2>
          <span :class="product.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'" class="shrink-0 inline-flex rounded-full px-2.5 py-1 text-xs font-medium">
            {{ product.active ? 'Active' : 'Inactive' }}
          </span>
        </div>
        <p class="mt-2 text-sm text-gray-500 min-h-10">{{ product.description || 'No description added.' }}</p>
        <dl class="mt-5 grid grid-cols-3 gap-3 border-t border-gray-100 pt-4">
          <div><dt class="text-xs text-gray-500">Quantity</dt><dd class="mt-1 text-sm font-semibold text-gray-900">{{ formatNumber(product.quantity) }}</dd></div>
          <div><dt class="text-xs text-gray-500">Size</dt><dd class="mt-1 text-sm font-semibold text-gray-900">{{ product.size || '-' }}</dd></div>
          <div><dt class="text-xs text-gray-500">Price</dt><dd class="mt-1 text-sm font-semibold text-gray-900">₹{{ formatNumber(product.price) }}</dd></div>
        </dl>
        <div class="mt-5 flex items-center justify-end gap-4 border-t border-gray-100 pt-4">
          <button type="button" @click="editProduct(product)" class="text-sm font-medium text-indigo-600 hover:text-indigo-900">Edit</button>
          <button type="button" @click="removeProduct(product)" class="text-sm font-medium text-red-600 hover:text-red-900">Delete</button>
        </div>
      </article>
      <div v-if="store.products.length === 0" class="md:col-span-2 xl:col-span-3 bg-white rounded-xl shadow p-12 text-center text-gray-500">
        No products found. Add your first product above.
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useToast } from 'vue-toastification'
import { useMilkStore } from '../stores/milkStore'

const store = useMilkStore()
const toast = useToast()
const editing = ref(false)
const saving = ref(false)

const defaultForm = () => ({
  product_name: '',
  description: '',
  quantity: 0,
  size: '',
  price: 0,
  active: true
})
const form = ref(defaultForm())

const formatNumber = value => Number(value || 0).toFixed(2)

const resetForm = () => {
  form.value = defaultForm()
  editing.value = false
}

const editProduct = product => {
  form.value = { ...product }
  editing.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const saveProduct = async () => {
  saving.value = true
  try {
    if (editing.value) {
      await store.updateProduct(form.value.id, form.value)
      toast.success('Product updated')
    } else {
      await store.createProduct(form.value)
      toast.success('Product added')
    }
    resetForm()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to save product')
  } finally {
    saving.value = false
  }
}

const removeProduct = async product => {
  if (!window.confirm(`Delete ${product.product_name}?`)) return
  try {
    await store.deleteProduct(product.id)
    toast.success('Product deleted')
    if (form.value.id === product.id) resetForm()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'Unable to delete product')
  }
}

onMounted(() => store.fetchProducts())
</script>

<style scoped>
.form-input {
  @apply w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-indigo-500;
}

.button-primary {
  @apply rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50;
}

.button-secondary {
  @apply rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50;
}
</style>
