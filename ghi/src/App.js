import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "./Auth/PrivateRoute";
import MainPage from "./MainPages/MainPage";
import { AuthProvider } from "./context/AuthContext";
import Nav from "./MainPages/Nav";
import TravelDetailPage from "./MainPages/TravelDetailPage";
import Login from "./Auth/Login";
import SignUp from "./Auth/SignUp";
import TestComponent from "./Auth/TestComponent";
import { PackingLists } from "./MainPages/PackingLists";
import DetailList from "./MainPages/DetailList";
import { createElement } from "react";
import Footer from "./MainPages/Footer.js";


export default function App(props) {
  // when running App for testing, App.test.js will pass in MockAuthProvider
  // to bypass need for user data
  // if nothing is passed into props, then authProvider will default to AuthProvider
  const { authProvider = AuthProvider } = props;

  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, "");

  // abstract Components
  const navAndRoutes = (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<MainPage />} exact />
        <Route path="/travel_details" element={<TravelDetailPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route
          path="/test-component"
          element={
            <PrivateRoute>
              <TestComponent />
            </PrivateRoute>
          }
        />
        <Route path="/packinglists" element={<PrivateRoute><PackingLists /></PrivateRoute>} />
        <Route path="/packing_list" element={<DetailList />} />
      </Routes>
      <Footer />
    </>
  );

  // can not simply plug in authProvider variable as a component, so
  // using createElemnent to create a new react element to include
  // authProvider
  return (
    
    <BrowserRouter basename={basename}>
      {createElement(authProvider, {}, navAndRoutes)}
    </BrowserRouter>
    
  );

}
