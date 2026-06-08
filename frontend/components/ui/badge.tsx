import { cn } from "@/lib/utils";

interface BadgeProps {
  className?: string;
  children: React.ReactNode;
  variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
}

export function Badge({ className, children, variant = "default" }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors",
        {
          "border-transparent bg-blue-600 text-white": variant === "default",
          "border-transparent bg-gray-100 text-gray-900": variant === "secondary",
          "border-transparent bg-red-600 text-white": variant === "destructive",
          "border-transparent bg-green-600 text-white": variant === "success",
          "border-transparent bg-yellow-600 text-white": variant === "warning",
          "border-gray-200 text-gray-900": variant === "outline",
        },
        className
      )}
    >
      {children}
    </span>
  );
}
