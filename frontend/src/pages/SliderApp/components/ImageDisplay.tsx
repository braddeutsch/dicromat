import styles from '../SliderApp.module.css';

interface ImageDisplayProps {
  imageBase64: string | null;
  isLoading: boolean;
}

export function ImageDisplay({ imageBase64, isLoading }: ImageDisplayProps) {
  return (
    <div className={styles.imageContainer}>
      {isLoading && (
        <div className={styles.loadingOverlay}>
          <div className={styles.spinner} />
        </div>
      )}
      {imageBase64 ? (
        <img
          src={`data:image/png;base64,${imageBase64}`}
          alt="Generated colorblind test pattern"
          className={styles.generatedImage}
        />
      ) : (
        <div className={styles.placeholder}>
          <p>Adjust parameters to generate an image</p>
        </div>
      )}
    </div>
  );
}
