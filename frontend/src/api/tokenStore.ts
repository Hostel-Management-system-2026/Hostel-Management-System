const ACCESS_KEY = 'hms.access'
const REFRESH_KEY = 'hms.refresh'

export type TokenPair = { access: string; refresh: string }

export const tokenStore = {
  getAccess: () => sessionStorage.getItem(ACCESS_KEY),
  getRefresh: () => sessionStorage.getItem(REFRESH_KEY),
  set: ({ access, refresh }: TokenPair) => {
    sessionStorage.setItem(ACCESS_KEY, access)
    sessionStorage.setItem(REFRESH_KEY, refresh)
  },
  setAccess: (access: string) => sessionStorage.setItem(ACCESS_KEY, access),
  clear: () => {
    sessionStorage.removeItem(ACCESS_KEY)
    sessionStorage.removeItem(REFRESH_KEY)
  },
}
