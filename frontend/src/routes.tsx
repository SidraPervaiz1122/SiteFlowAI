import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Layout } from './components/layout/Layout';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Boq } from './pages/Boq';
import { BoqItemDetail } from './pages/BoqItem';
import { CheckRequests } from './pages/CheckRequests';
import { CheckRequestDetail } from './pages/CheckRequestDetail';
import { Inspections } from './pages/Inspections';
import { InspectionDetail } from './pages/InspectionDetail';
import { Approvals } from './pages/Approvals';
import { IpcPage } from './pages/Ipc';
import { IpcDetail } from './pages/IpcDetail';
import { Documents } from './pages/Documents';
import { AiAssistant } from './pages/AiAssistant';
import { Activity } from './pages/Activity';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) {
    return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading SiteFlow AI...</div>;
  }
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="boq" element={<Boq />} />
        <Route path="boq/:id" element={<BoqItemDetail />} />
        <Route path="check-requests" element={<CheckRequests />} />
        <Route path="check-requests/:id" element={<CheckRequestDetail />} />
        <Route path="inspections" element={<Inspections />} />
        <Route path="inspections/:id" element={<InspectionDetail />} />
        <Route path="approvals" element={<Approvals />} />
        <Route path="ipc" element={<IpcPage />} />
        <Route path="ipc/:id" element={<IpcDetail />} />
        <Route path="documents" element={<Documents />} />
        <Route path="ai" element={<AiAssistant />} />
        <Route path="activity" element={<Activity />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
