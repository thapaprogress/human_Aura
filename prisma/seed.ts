import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seed...\n');

  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 10);
  const admin = await prisma.user.upsert({
    where: { email: 'admin@auracamera.app' },
    update: {},
    create: {
      email: 'admin@auracamera.app',
      passwordHash: adminPassword,
      firstName: 'Admin',
      lastName: 'User',
      subscriptionTier: 'yearly',
      subscriptionStatus: 'active',
      isActive: true,
    },
  });
  console.log('✅ Created admin user:', admin.email);

  // Create test user
  const testPassword = await bcrypt.hash('test123', 10);
  const testUser = await prisma.user.upsert({
    where: { email: 'test@example.com' },
    update: {},
    create: {
      email: 'test@example.com',
      passwordHash: testPassword,
      firstName: 'Test',
      lastName: 'User',
      subscriptionTier: 'monthly',
      subscriptionStatus: 'active',
      isActive: true,
    },
  });
  console.log('✅ Created test user:', testUser.email);

  // Create free tier user
  const freePassword = await bcrypt.hash('free123', 10);
  const freeUser = await prisma.user.upsert({
    where: { email: 'free@example.com' },
    update: {},
    create: {
      email: 'free@example.com',
      passwordHash: freePassword,
      firstName: 'Free',
      lastName: 'User',
      subscriptionTier: 'free',
      subscriptionStatus: 'inactive',
      isActive: true,
    },
  });
  console.log('✅ Created free tier user:', freeUser.email);

  // Create sample aura profile for test user
  const sampleSession = await prisma.session.create({
    data: {
      userId: testUser.id,
      status: 'completed',
      faceDetected: true,
      alignmentScore: 0.92,
      biofeedbackDurationMs: 5000,
      mode: 'selfie',
      completedAt: new Date(),
    },
  });

  const sampleAuraProfile = await prisma.auraProfile.create({
    data: {
      sessionId: sampleSession.id,
      userId: testUser.id,
      majorityColor: 'violet',
      majorityPercentage: 45.5,
      moderateColors: JSON.stringify(['indigo', 'blue']),
      moderatePercentages: JSON.stringify([28.3, 18.7]),
      minorityColors: JSON.stringify(['white', 'gold', 'silver']),
      minorityPercentages: JSON.stringify([4.2, 2.1, 1.2]),
      intensity: 78.5,
      brightness: 82.0,
      saturation: 65.3,
      positioning: JSON.stringify({
        ascendant: ['blue', 'white'],
        descendant: ['indigo', 'silver'],
        cathedra: ['violet'],
        coronation: ['gold'],
        etherea: ['violet', 'indigo', 'blue'],
      }),
      profileData: JSON.stringify({
        overallEnergy: 'spiritual',
        dominantChakra: 'crown',
        emotionalState: 'peaceful',
        spiritualGrowth: 'advanced',
      }),
    },
  });

  // Create sample reading
  await prisma.reading.create({
    data: {
      auraProfileId: sampleAuraProfile.id,
      sessionId: sampleSession.id,
      userId: testUser.id,
      section: 'color_analysis',
      title: 'Your Dominant Colors',
      content: 'Your aura reveals a beautiful violet dominant energy, indicating deep spiritual awareness and intuitive abilities. This violet presence suggests you are highly connected to your higher consciousness and possess natural wisdom. The supporting indigo and blue energies enhance your intuitive and communicative abilities, creating a harmonious blend of spiritual insight and clear expression.',
      colorReferences: JSON.stringify(['violet', 'indigo', 'blue', 'white', 'gold', 'silver']),
      generatedBy: 'ai',
    },
  });

  await prisma.reading.create({
    data: {
      auraProfileId: sampleAuraProfile.id,
      sessionId: sampleSession.id,
      userId: testUser.id,
      section: 'alignment',
      title: 'Your Energy Alignment',
      content: 'Your ascendant energy (right side) shows blue and white, indicating you are currently receptive to truth and purity in your environment. Your descendant energy (left side) displays indigo and silver, showing you are expressing deep intuition and reflective wisdom to others. The coronation at the top reveals gold energy, suggesting spiritual mastery and enlightened consciousness in your thoughts.',
      colorReferences: JSON.stringify(['blue', 'white', 'indigo', 'silver', 'gold', 'violet']),
      generatedBy: 'ai',
    },
  });

  await prisma.reading.create({
    data: {
      auraProfileId: sampleAuraProfile.id,
      sessionId: sampleSession.id,
      userId: testUser.id,
      section: 'guidance',
      title: 'Your Spiritual Guidance',
      content: 'Your aura suggests you are in a phase of significant spiritual growth. The strong violet and indigo combination indicates your third eye and crown chakras are highly active. This is an excellent time for meditation, spiritual study, and developing your intuitive abilities. Trust your inner guidance and allow your natural wisdom to flow. Your presence brings a calming, enlightened energy to those around you.',
      colorReferences: JSON.stringify(['violet', 'indigo']),
      generatedBy: 'ai',
    },
  });

  console.log('✅ Created sample aura profile and readings for test user');

  console.log('\n✨ Database seed completed successfully!');
  console.log('\nTest accounts:');
  console.log('  Admin: admin@auracamera.app / admin123');
  console.log('  Test:  test@example.com / test123');
  console.log('  Free:  free@example.com / free123');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
