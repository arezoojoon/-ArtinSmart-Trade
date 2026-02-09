import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Login - TradeMate AI",
    description: "Secure Login to your TradeMate Dashboard",
};

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen flex-col items-center justify-center py-12 sm:px-6 lg:px-8 bg-background">
            {children}
        </div>
    );
}
