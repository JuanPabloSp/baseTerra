output "resource_group_name" {
  description = "The name of the created resource group"
  value       = azurerm_resource_group.rg.name
}

output "public_ip_address" {
  description = "The public IP address of the virtual machine"
  value       = azurerm_windows_virtual_machine.main.public_ip_address
}

output "admin_password" {
  description = "The admin password for the virtual machine"
  sensitive   = true
  value       = azurerm_windows_virtual_machine.main.admin_password
}
