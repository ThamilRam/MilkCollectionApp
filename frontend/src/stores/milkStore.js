import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const useMilkStore = defineStore('milk', {
  state: () => ({
    customers: [],
    products: [],
    purchases: [],
    entries: [],
    payments: [],
    dashboard: null,
    dateWiseData: [],
    customerMonthlyData: [],
    topCustomers: [],
    customerPortal: null,
    paymentContext: {
      customer_id: '',
      from_date: '',
      end_date: '',
      amount: 0
    },
    loading: false,
    error: null
  }),
  getters: {
    activeCustomers: (state) => state.customers.filter(c => c.status === 'Active'),
    customerOptions: (state) => state.customers.map(c => ({
      value: c.customer_id,
      label: `${c.customer_id} - ${c.name}`
    })),
    milkCustomerOptions: (state) => state.customers
      .filter(c => c.isMilkcustomer !== false)
      .map(c => ({
        value: c.customer_id,
        label: `${c.customer_id} - ${c.name}`
      }))
  },
  actions: {
    async fetchCustomers() {
      this.loading = true
      try {
        const { data } = await axios.get(`${API_URL}/customers`)
        this.customers = data
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    async fetchProducts() {
      this.loading = true
      try {
        const { data } = await axios.get(`${API_URL}/products`)
        this.products = data
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },
    async createProduct(product) {
      const { data } = await axios.post(`${API_URL}/products`, product)
      this.products.push(data)
      return data
    },
    async updateProduct(id, product) {
      const { data } = await axios.put(`${API_URL}/products/${id}`, product)
      const index = this.products.findIndex(item => item.id === id)
      if (index !== -1) this.products[index] = data
      return data
    },
    async deleteProduct(id) {
      await axios.delete(`${API_URL}/products/${id}`)
      this.products = this.products.filter(item => item.id !== id)
    },
    async fetchPurchases(customerId) {
      const { data } = await axios.get(`${API_URL}/purchases`, { params: { customer_id: customerId } })
      this.purchases = data
    },
    async createPurchase(purchase) {
      const { data } = await axios.post(`${API_URL}/purchases`, purchase)
      this.purchases.unshift(data)
      const product = this.products.find(item => item.id === purchase.product_id)
      if (product) product.quantity = Number(product.quantity) - Number(purchase.quantity)
      return data
    },
    async updatePurchasePaid(id, paid) {
      const { data } = await axios.patch(`${API_URL}/purchases/${id}`, { paid })
      const index = this.purchases.findIndex(item => item.id === id)
      if (index !== -1) this.purchases[index] = data
      return data
    },
    async deletePurchase(id) {
      await axios.delete(`${API_URL}/purchases/${id}`)
      this.purchases = this.purchases.filter(item => item.id !== id)
    },
    async fetchEntries(params = {}) {
      this.loading = true
      try {
        const { data } = await axios.get(`${API_URL}/daily-entries`, { params })
        this.entries = data
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },
    async createEntry(entry) {
      const { data } = await axios.post(`${API_URL}/daily-entries`, entry)
      return data
    },
    async deleteEntry(id) {
      await axios.delete(`${API_URL}/daily-entries/${id}`)
    },
    async fetchPayments(customerId = null) {
      const params = customerId ? { customer_id: customerId } : {}
      const { data } = await axios.get(`${API_URL}/payment-records`, { params })
      this.payments = data
    },
    async createPayment(payment) {
      const { data } = await axios.post(`${API_URL}/payment-records`, payment)
      return data
    },
    setPaymentContext(context) {
      this.paymentContext = {
        customer_id: context.customer_id || '',
        from_date: context.from_date || '',
        end_date: context.end_date || '',
        amount: context.amount != null ? context.amount : 0
      }
    },
    async deletePayment(id) {
      await axios.delete(`${API_URL}/payment-records/${id}`)
    },
    async fetchDashboard() {
      const { data } = await axios.get(`${API_URL}/dashboard/summary`)
      this.dashboard = data
    },
    async fetchDateWise(params = {}) {
      const { data } = await axios.get(`${API_URL}/dashboard/date-wise`, { params })
      this.dateWiseData = data
    },
    async fetchCustomerMonthly(customerId, year = null) {
      const params = { customer_id: customerId }
      if (year) params.year = year
      const { data } = await axios.get(`${API_URL}/dashboard/customer-monthly`, { params })
      this.customerMonthlyData = data
    },
    async fetchTopCustomers(month = null, year = null) {
      const params = {}
      if (month) params.month = month
      if (year) params.year = year
      const { data } = await axios.get(`${API_URL}/dashboard/top-customers`, { params })
      this.topCustomers = data
    },
    async fetchCustomerPortal(customerId, params = {}) {
      const { data } = await axios.get(`${API_URL}/customer-portal/${customerId}`, { params })
      this.customerPortal = data
    },
    async createCustomer(customer) {
      const { data } = await axios.post(`${API_URL}/customers`, customer)
      this.customers.push(data)
      return data
    },
    async updateCustomer(id, customer) {
      const { data } = await axios.put(`${API_URL}/customers/${id}`, customer)
      const idx = this.customers.findIndex(c => c.customer_id === id)
      if (idx !== -1) this.customers[idx] = data
      return data
    }
  }
})