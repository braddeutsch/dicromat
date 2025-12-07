import { BrowserRouter } from 'react-router-dom';
import { TestProvider } from './context';
import { AppRoutes } from './routes/AppRoutes';
import './styles/global.css';

export function App() {
  return (
    <BrowserRouter>
      <TestProvider>
        <AppRoutes />
      </TestProvider>
    </BrowserRouter>
  );
}
