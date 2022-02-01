provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ism-va-iaac-eastus" {
  name     = "ism-va-iaac-eastus"
  location = "EAST US"
}

resource "azurerm_virtual_network" "cloud-shell-storage-eastus-vnet-umair" {
  name                = "cloud-shell-storage-eastus-vnet-umair"
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.8", "10.0.0.9"]
}

resource "azurerm_sql_server" "virutal-umair" {
  name                         = "virutal-umair"
  resource_group_name          = azurerm_resource_group.ism-va-iaac-eastus.name
  location                     = azurerm_resource_group.ism-va-iaac-eastus.location
  version                      = "12.0"
  administrator_login          = "umairdb"
  administrator_login_password = "umair@123"
}

resource "azurerm_sql_database" "COVID19-db-umair" {
  name                = "COVID19-db-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  server_name         = azurerm_sql_server.virutal-umair.name
}

resource "azurerm_storage_account" "htmltriggeringlothub-umair" {
  name                     = "htmltriggeringlothub-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account" "sensorstorage-umair" {
  name                     = "sensorstorage-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "htmltriggeringlothub-umair" {
  name                = "htmltriggeringlothub-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  application_type    = "web"
}

resource "azurerm_application_insights" "ismileqna-umair" {
  name                = "ismileqna-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  application_type    = "web"
}

resource "azurerm_application_insights" "ismileqna-bot-umair" {
  name                = "ismileqna-bot"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  application_type    = "web"
}

resource "azurerm_iothub" "iotcloudhub-umair" {
  name                = "iotcloudhub-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location

  sku {
    name     = "F1"
    capacity = "1"
  }
}

resource "azurerm_app_service_plan" "virtualassistant-eus-appserviceplan-umair" {
  name                = "virtualassistant-eus-appserviceplan-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "virtualassistant-eus-bothandle-umair" {
  name                = "virtualassistant-eus-bothandle-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  app_service_plan_id = azurerm_app_service_plan.virtualassistant-eus-appserviceplan-umair.id
}

resource "azurerm_app_service_plan" "ismileqna-umair" {
  name                = "ismileqna-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "ismileqna-umair" {
  name                = "ismileqna-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  app_service_plan_id = azurerm_app_service_plan.ismileqna-umair.id
}

resource "azurerm_cognitive_account" "ismileqna-umair" {
  name                = "ismileqna-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  kind                = "CognitiveServices"
  sku_name = "S0"
}

resource "azurerm_app_service_plan" "ASP-cloudshellstorageeast-b1a5-umair" {
  name                = "ASP-cloudshellstorageeast-b1a5-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "OneModel-umair" {
  name                = "OneModel-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_app_service_plan" "ASP-ismileqna-bot-a48b-umair" {
  name                = "ASP-ismileqna-bot-a48b-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service_plan" "plan-win-HeathBotContainerSample2910-umair" {
  name                = "plan-win-HeathBotContainerSample2910-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "faceDemoTest2-umair" {
  name                = "faceDemoTest2-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  app_service_plan_id = azurerm_app_service_plan.plan-win-HeathBotContainerSample2910-umair.id
}

resource "azurerm_sql_database" "iotsensordata-umair" {
  name                = "iotsensordata-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  server_name         = azurerm_sql_server.virutal-umair.name
}

resource "azurerm_app_service" "throat-umair" {
  name                = "throat-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_stream_analytics_job" "imagestreaming-umair" {
  name                                     = "imagestreaming-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  compatibility_level                      = "1.1"
  streaming_units                          = 3

  transformation_query = <<QUERY
    SELECT *
    INTO [YourOutputAlias]
    FROM [YourInputAlias]
QUERY

}

resource "azurerm_search_service" "ismileqna-asimhib7jc6fvwc-umair" {
  name                = "ismileqna-asimhib7jc6fvwc-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  sku                 = "free"
}

resource "azurerm_app_service" "mainwebui-umair" {
  name                = "mainwebui-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_app_service" "Xraymodel-umair" {
  name                = "Xraymodel-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_app_service" "locatorApp-umair" {
  name                = "locatorApp-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_storage_account" "xray-umair" {
  name                     = "xray-umair"
  resource_group_name      = azurerm_resource_group.ism-va-iaac-eastus.name
  location                 = azurerm_resource_group.ism-va-iaac-eastus.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
}

resource "azurerm_storage_container" "xray-container-umair" {
  name                  = "xray-container-umair"
  storage_account_name  = azurerm_storage_account.xray-umair.name
  container_access_type = "blob"
}


resource "azurerm_app_service" "voicexray-umair" {
  name                = "voicexray-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "Central US"
  app_service_plan_id = azurerm_app_service_plan.ASP-cloudshellstorageeast-b1a5-umair.id
}

resource "azurerm_cognitive_account" "LanguageUnderstandingforvirtualassistant-Authoring-umair" {
  name                = "LanguageUnderstandingforvirtualassistant-Authoring-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = "West US"
  kind                = "LUIS.Authoring"
  sku_name = "F0"
}

resource "azurerm_cognitive_account" "LanguageUnderstandingforvirtualassistant-umair" {
  name                = "LanguageUnderstandingforvirtualassistant-umair"
  resource_group_name = azurerm_resource_group.ism-va-iaac-eastus.name
  location            = azurerm_resource_group.ism-va-iaac-eastus.location
  kind                = "LUIS"
  sku_name = "F0"
}

