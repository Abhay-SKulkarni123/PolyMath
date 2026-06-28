import { useState, useCallback } from 'react'

interface ValidationRule {
  required?: boolean
  minLength?: number
  maxLength?: number
  pattern?: RegExp
  email?: boolean
  min?: number
  max?: number
  custom?: (value: any) => string | null
}

interface ValidationRules {
  [key: string]: ValidationRule
}

interface FormErrors {
  [key: string]: string
}

interface FormTouched {
  [key: string]: boolean
}

export function useFormValidation<T extends Record<string, any>>(
  initialValues: T,
  validationRules: ValidationRules
) {
  const [values, setValues] = useState<T>(initialValues)
  const [errors, setErrors] = useState<FormErrors>({})
  const [touched, setTouched] = useState<FormTouched>({})

  const validateField = useCallback(
    (name: string, value: any): string | null => {
      const rules = validationRules[name]
      if (!rules) return null

      // Required check
      if (rules.required && (!value || value.toString().trim() === '')) {
        return 'This field is required'
      }

      // Skip other validations if empty and not required
      if (!value || value.toString().trim() === '') {
        return null
      }

      // Min length
      if (rules.minLength && value.toString().length < rules.minLength) {
        return `Must be at least ${rules.minLength} characters`
      }

      // Max length
      if (rules.maxLength && value.toString().length > rules.maxLength) {
        return `Must be no more than ${rules.maxLength} characters`
      }

      // Email pattern
      if (rules.email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
        if (!emailPattern.test(value)) {
          return 'Invalid email address'
        }
      }

      // Custom pattern
      if (rules.pattern && !rules.pattern.test(value)) {
        return 'Invalid format'
      }

      // Min number
      if (rules.min !== undefined && Number(value) < rules.min) {
        return `Must be at least ${rules.min}`
      }

      // Max number
      if (rules.max !== undefined && Number(value) > rules.max) {
        return `Must be no more than ${rules.max}`
      }

      // Custom validation
      if (rules.custom) {
        return rules.custom(value)
      }

      return null
    },
    [validationRules]
  )

  const validateAll = useCallback((): boolean => {
    const newErrors: FormErrors = {}
    let isValid = true

    Object.keys(validationRules).forEach((name) => {
      const error = validateField(name, values[name])
      if (error) {
        newErrors[name] = error
        isValid = false
      }
    })

    setErrors(newErrors)
    return isValid
  }, [values, validationRules, validateField])

  const handleChange = useCallback(
    (name: string, value: any) => {
      setValues((prev) => ({ ...prev, [name]: value }))
      
      // Validate on change if field has been touched
      if (touched[name]) {
        const error = validateField(name, value)
        setErrors((prev) => ({
          ...prev,
          [name]: error || '',
        }))
      }
    },
    [touched, validateField]
  )

  const handleBlur = useCallback(
    (name: string) => {
      setTouched((prev) => ({ ...prev, [name]: true }))
      const error = validateField(name, values[name])
      setErrors((prev) => ({
        ...prev,
        [name]: error || '',
      }))
    },
    [values, validateField]
  )

  const resetForm = useCallback(() => {
    setValues(initialValues)
    setErrors({})
    setTouched({})
  }, [initialValues])

  const setFieldValue = useCallback((name: string, value: any) => {
    setValues((prev) => ({ ...prev, [name]: value }))
  }, [])

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateAll,
    resetForm,
    setFieldValue,
    setValues,
  }
}

// Common validation rules
export const commonRules = {
  required: { required: true },
  email: { required: true, email: true },
  password: {
    required: true,
    minLength: 8,
    custom: (value: string) => {
      if (!/(?=.*[a-z])/.test(value)) {
        return 'Password must contain at least one lowercase letter'
      }
      if (!/(?=.*[A-Z])/.test(value)) {
        return 'Password must contain at least one uppercase letter'
      }
      if (!/(?=.*\d)/.test(value)) {
        return 'Password must contain at least one number'
      }
      return null
    },
  },
  confirmPassword: (password: string) => ({
    required: true,
    custom: (value: string) => {
      if (value !== password) {
        return 'Passwords do not match'
      }
      return null
    },
  }),
}