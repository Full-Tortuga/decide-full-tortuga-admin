import { TabView } from "primereact/tabview";
import "../css/Views.css";

const Views = ({ children }) => {
  return (
    <div className="tabview-demo">
      <TabView className="tabview-custom">{children}</TabView>
    </div>
  );
};

export default Views;
