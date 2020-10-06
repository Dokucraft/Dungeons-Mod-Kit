
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "UObject/SoftObjectPath.h"
#include "CustomStructs.generated.h"

USTRUCT(BlueprintType)
struct FSkinEntry : public FTableRowBase {
	GENERATED_BODY()

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FSoftObjectPath AvatarMaterial;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FSoftObjectPath PortraitMaterial;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RequiredEntitlement;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Order;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool ConsiderForDefault;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool IsReleased;

};

UENUM()
enum ECosmeticType {
	Pet,
	Cape
};

USTRUCT(BlueprintType)
struct FCosmeticsEntry : public FTableRowBase {
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FText DisplayName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FText DisplayDescription;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSoftObjectPath IconTexture;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSoftObjectPath EquippedSound;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSoftObjectPath EquippedAnimation;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSoftObjectPath BlueprintClass;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Entitlement;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TEnumAsByte<ECosmeticType> Type;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float PreferredInventoryCharacterRotation;

  UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool IsReleased;

};
