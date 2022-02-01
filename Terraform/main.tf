provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "cloud-shell-storage-eastus" {
  name     = "cloud-shell-storage-eastus-prasad"
  location = "EAST US"
}

resource "azurerm_virtual_network" "cloud-shell-storage-eastus-vnet" {
  name                = "cloud-shell-storage-eastus-vnet"
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  address_space       = ["10.0.0.0/24"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]
}

resource "azurerm_sql_server" "virutal-prasad" {
  name                         = "virutal-prasad"
  resource_group_name          = azurerm_resource_group.cloud-shell-storage-eastus.name
  location                     = azurerm_resource_group.cloud-shell-storage-eastus.location
  version                      = "12.0"
  administrator_login          = "Ismiledb"
  administrator_login_password = "Ismile@123"
}

resource "azurerm_sql_database" "COVID19-db" {
  name                = "COVID19-db"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  server_name         = azurerm_sql_server.virutal-prasad.name
}

resource "azurerm_storage_account" "htmltriggeringlothub" {
  name                     = "htmltriggeringlothub"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account" "sensorstorage" {
  name                     = "sensorstorage"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "htmltriggeringlothub" {
  name                = "htmltriggeringlothub"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  application_type    = "web"
}

resource "azurerm_application_insights" "ismileqna" {
  name                = "ismileqna"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  application_type    = "web"
}

resource "azurerm_application_insights" "ismileqna-bot" {
  name                = "ismileqna-bot"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  application_type    = "web"
}

resource "azurerm_iothub" "iotcloudhub" {
  name                = "iotcloudhub"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location

  sku {
    name     = "F1"
    capacity = "1"
  }
}

resource "azurerm_app_service_plan" "virtualassistant-eus-appserviceplan" {
  name                = "virtualassistant-eus-appserviceplan"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "virtualassistant-eus-bothandle" {
  name                = "virtualassistant-eus-bothandle"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  app_service_plan_id = azurerm_app_service_plan.virtualassistant-eus-appserviceplan.id
}

resource "azurerm_app_service_plan" "ismileqna" {
  name                = "ismileqna"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "ismileqna" {
  name                = "ismileqna"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  app_service_plan_id = azurerm_app_service_plan.ismileqna.id
}

resource "azurerm_cognitive_account" "ismileqna" {
  name                = "ismileqna"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  kind                = "CognitiveServices"
  sku_name = "S0"
}

resource "azurerm_app_service_plan" "ASP-cloudshellstorageeast-b1a5" {
  name                = "ASP-cloudshellstorageeast-b1a5"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "OneModel" {
  name                = "OneModel"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_app_service_plan" "ASP-ismileqna-bot-a48b" {
  name                = "ASP-ismileqna-bot-a48b"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service_plan" "plan-win-HeathBotContainerSample2910" {
  name                = "plan-win-HeathBotContainerSample2910"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "faceDemoTest2" {
  name                = "faceDemoTest2"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  app_service_plan_id = azurerm_app_service_plan.plan-win-HeathBotContainerSample2910.id
}

resource "azurerm_sql_database" "iotsensordata" {
  name                = "iotsensordata"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  server_name         = azurerm_sql_server.virutal-prasad.name
}

resource "azurerm_app_service" "throat" {
  name                = "throat"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_stream_analytics_job" "imagestreaming" {
  name                                     = "imagestreaming"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  compatibility_level                      = "1.1"
  streaming_units                          = 3

  transformation_query = <<QUERY
    SELECT *
    INTO [YourOutputAlias]
    FROM [YourInputAlias]
QUERY

}

resource "azurerm_search_service" "ismileqna-asimhib7jc6fvwc" {
  name                = "ismileqna-asimhib7jc6fvwc"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  sku                 = "free"
}

resource "azurerm_app_service" "mainwebui" {
  name                = "mainwebui"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_app_service" "Xraymodel" {
  name                = "Xraymodel"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_app_service" "locatorApp" {
  name                = "locatorApp"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_storage_account" "xray" {
  name                     = "xray"
  resource_group_name      = azurerm_resource_group.cloud-shell-storage-eastus.name
  location                 = azurerm_resource_group.cloud-shell-storage-eastus.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
}

resource "azurerm_storage_container" "xray-container" {
  name                  = "xray-container"
  storage_account_name  = azurerm_storage_account.xray.name
  container_access_type = "blob"
}


resource "azurerm_app_service" "voicexray" {
  name                = "voicexray"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5.id
}

resource "azurerm_cognitive_account" "LanguageUnderstandingforvirtualassistant-Authoring" {
  name                = "LanguageUnderstandingforvirtualassistant-Authoring"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = "West US"
  kind                = "LUIS.Authoring"
  sku_name = "F0"
}

resource "azurerm_cognitive_account" "LanguageUnderstandingforvirtualassistant" {
  name                = "LanguageUnderstandingforvirtualassistant"
  resource_group_name = azurerm_resource_group.cloud-shell-storage-eastus.name
  location            = azurerm_resource_group.cloud-shell-storage-eastus.location
  kind                = "LUIS"
  sku_name = "F0"
}

