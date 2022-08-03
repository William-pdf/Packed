import { TripForm } from "./TripForm";
import "./pages.css";

export default function MainPage() {
  return (
    <div className="px-4 py-5 my-5 text-center main-page-background shadow">
      <div className="row">
        <div className="col-4">
          <h3 className="app-blurb">helping you get </h3>
          <h1>packed</h1>
          <h3>for your next trip</h3>
        </div>
        <div className="col">
          <TripForm />
        </div>
      </div>
      <div className="row">
        <img className="group-pic" src="../group.png" alt="group" />
      </div>
    </div>
  );
}
