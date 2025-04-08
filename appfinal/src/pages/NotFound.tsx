
import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-spanish-cream">
      <div className="text-center p-8 bg-white rounded-lg shadow-sm max-w-md">
        <h1 className="text-6xl font-bold text-spanish-red mb-4">404</h1>
        <p className="text-xl text-spanish-navy mb-6">¡Ay caramba! This page doesn't exist.</p>
        <p className="mb-8 text-muted-foreground">
          The page you're looking for couldn't be found. Let's get you back on track.
        </p>
        <Link to="/">
          <Button className="bg-spanish-red hover:bg-spanish-red/90">
            Return to Home
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;