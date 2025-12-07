import { useState, useEffect, type FormEvent, type ChangeEvent } from 'react';
import { Button } from './Button';
import styles from './AnswerInput.module.css';

interface AnswerInputProps {
  onSubmit: (answer: number | null) => void;
  isSubmitting: boolean;
  imageNumber: number;
}

export function AnswerInput({ onSubmit, isSubmitting, imageNumber }: AnswerInputProps) {
  const [numberValue, setNumberValue] = useState('');
  const [noNumberVisible, setNoNumberVisible] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setNumberValue('');
    setNoNumberVisible(false);
    setError('');
  }, [imageNumber]);

  const handleNumberChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || /^\d{0,2}$/.test(value)) {
      setNumberValue(value);
      setNoNumberVisible(false);
      setError('');
    }
  };

  const handleCheckboxChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNoNumberVisible(e.target.checked);
    if (e.target.checked) {
      setNumberValue('');
      setError('');
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (!noNumberVisible && numberValue === '') {
      setError('Please enter a number or select "I don\'t see a number"');
      return;
    }

    if (!noNumberVisible) {
      const num = parseInt(numberValue, 10);
      if (isNaN(num) || num < 0 || num > 99) {
        setError('Please enter a number between 0 and 99');
        return;
      }
      onSubmit(num);
    } else {
      onSubmit(null);
    }
  };

  const isValid = noNumberVisible || (numberValue !== '' && /^\d{1,2}$/.test(numberValue));

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <label className={styles.label} htmlFor="answer-input">
        What number do you see?
      </label>
      
      <div className={styles.inputContainer}>
        <input
          id="answer-input"
          type="text"
          inputMode="numeric"
          pattern="[0-9]*"
          className={`${styles.input} ${error ? styles.inputError : ''}`}
          value={numberValue}
          onChange={handleNumberChange}
          disabled={noNumberVisible || isSubmitting}
          placeholder="0-99"
          autoComplete="off"
          autoFocus
        />
      </div>

      <label className={styles.checkboxLabel}>
        <input
          type="checkbox"
          checked={noNumberVisible}
          onChange={handleCheckboxChange}
          disabled={isSubmitting}
          className={styles.checkbox}
        />
        <span>I don't see a number</span>
      </label>

      {error && (
        <p className={styles.error} role="alert">{error}</p>
      )}

      <Button
        type="submit"
        disabled={!isValid}
        isLoading={isSubmitting}
        size="large"
      >
        Submit Answer
      </Button>
    </form>
  );
}
